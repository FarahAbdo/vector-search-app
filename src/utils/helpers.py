import numpy as np
from typing import List

def calculate_cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def batch_process(items: List[str], batch_size: int = 32):
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]
