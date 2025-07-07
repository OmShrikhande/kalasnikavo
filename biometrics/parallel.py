"""
biometrics/parallel.py
Parallelization utilities for biometrics processing.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List, Any
import logging

def parallel_map(func: Callable, items: List[Any], max_workers: int = 4) -> List[Any]:
    """Run func on items in parallel and return results as a list."""
    results = [None] * len(items)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_idx = {executor.submit(func, item): idx for idx, item in enumerate(items)}
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                results[idx] = future.result()
            except Exception as e:
                logging.error(f"Parallel task failed: {e}")
                results[idx] = None
    return results
