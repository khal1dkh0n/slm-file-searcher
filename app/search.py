# app/search.py
# 
# Deprecated: search is now handled directly in api.py with FAISS

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def top_k_cosine(q_vec, mat, k=10):
    if mat is None or mat.shape[0]==0: return []
    sims=cosine_similarity(q_vec, mat)[0]
    idx=np.argsort(-sims)[:k]
    return [(int(i), float(sims[i])) for i in idx]