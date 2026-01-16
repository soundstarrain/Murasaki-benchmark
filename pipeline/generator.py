import asyncio
import os
import pandas as pd
import json
from openai import AsyncOpenAI
from tqdm.asyncio import tqdm

class LLMGenerator:
    def __init__(self, config):
        self.client = AsyncOpenAI(
            api_key=config['api_key'],
            base_url=config['base_url']
        )
        self.model_name = config['model_name']
        self.semaphore = asyncio.Semaphore(config.get('concurrency', 5))

    async def _call_api(self, text, system_prompt, max_tokens=None):
        async with self.semaphore:
            retries = 5
            for i in range(retries):
                try:
                    # Add timeout to prevent hanging indefinitely
                    response = await asyncio.wait_for(
                        self.client.chat.completions.create(
                            model=self.model_name,
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": text}
                            ],
                            temperature=1.0,
                            top_p=1.0,
                            max_tokens=max_tokens
                        ),
                        timeout=120 # Increased timeout for potential long generations
                    )

                    # Handle disparate response types
                    if isinstance(response, str):
                        # Try parsing as JSON first
                        try:
                            data = json.loads(response)
                            if "choices" in data:
                                return data["choices"][0]["message"]["content"].strip()
                            # If fallback to dict keys fails, maybe it matches other structures?
                        except:
                            pass
                        # If still string, assume it's the content (some proxies do this)
                        return response.strip()
                    
                    # If it's a dict (not Pydantic model) - rare but possible with some clients/wrappers
                    if isinstance(response, dict):
                        return response["choices"][0]["message"]["content"].strip()

                    # Standard Pydantic model
                    return response.choices[0].message.content.strip()

                except Exception as e:
                    if i < retries - 1:
                        wait_time = 2 * (2 ** i) # Exponential backoff: 2, 4, 8, 16...
                        print(f"Error {self.model_name} (Attempt {i+1}/{retries}): {e}. Retrying in {wait_time}s...")
                        await asyncio.sleep(wait_time)
                    else:
                        print(f"Failed {self.model_name} after {retries} attempts: {e}")
                        return "ERROR"
            return "ERROR"

    async def generate_batch(self, dataset, system_prompt, save_path=None):
        """
        Args:
            dataset: DataFrame containing 'src' and 'ref' columns
            system_prompt: System prompt string
            save_path: Optional path to save results incrementally (JSONL)
        Returns:
            DataFrame with original columns plus 'model_output' and 'model_name'
        """
        # 1. Load existing results to prevent duplicate calls (Idempotency)
        existing_srcs = set()
        if save_path and os.path.exists(save_path):
            try:
                # Determine format based on extension
                if save_path.endswith('.jsonl'):
                    with open(save_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.strip():
                                rec = json.loads(line)
                                if 'src' in rec:
                                    # Fix: Ignore ERROR outputs so they can be retried
                                    if rec.get('model_output', '') != "ERROR":
                                        existing_srcs.add(rec['src'])
                elif save_path.endswith('.csv'):
                     # Fallback for CSV
                     existing_df = pd.read_csv(save_path)
                     if 'src' in existing_df.columns:
                         existing_srcs.update(existing_df['src'].astype(str).tolist())
            except Exception as e:
                print(f"Warning: Could not read existing file for deduplication: {e}")
        
        print(f"Found {len(existing_srcs)} existing samples in {save_path}. These will be skipped.")

        file_lock = asyncio.Lock()

        async def process_row(index, row_data):
            src = row_data.get('src', '')
            
            # CHECK IDEMPOTENCY
            if src in existing_srcs:
                return "SKIPPED_EXISTING"

            category = row_data.get('category', 'Short') # Default to Short if missing
            category = row_data.get('category', 'Short') # Default to Short if missing
            
            # Dynamic Max Tokens based on Category
            token_limits = {
                "Short": 8000,
                "Medium": 4000,
                "Long": 30000
            }
            max_tokens = token_limits.get(category, 1000)

            # Specific overrides for models with lower limits
            if self.model_name in ["qwen3-8b", "Qwen3-8B"]:
                max_tokens = min(max_tokens, 8000)
            
            output = await self._call_api(src, system_prompt, max_tokens=max_tokens)
            
            if save_path:
                async with file_lock:
                    # Construct full row dict
                    save_row = row_data.to_dict()
                    save_row['model_output'] = output
                    save_row['model_name'] = self.model_name
                    
                    # Append to JSONL
                    with open(save_path, 'a', encoding='utf-8') as f:
                        f.write(json.dumps(save_row, ensure_ascii=False) + "\n")
            
            return output

        tasks = []
        for index, row in dataset.iterrows():
            tasks.append(process_row(index, row))
        
        results = await tqdm.gather(*tasks, desc=f"Generating {self.model_name}")
        
        output_df = dataset.copy()
        output_df['model_output'] = results
        output_df['model_name'] = self.model_name
        
        return output_df
