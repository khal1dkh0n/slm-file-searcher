# app/api.py
from fastapi import FastAPI
from pathlib import Path
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

app = FastAPI()

_model = None
_index = None
_records = None


def load_index(out: Path = Path("data/index")):
    global _model, _index, _records
    # Load model
    _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    # Load FAISS index
    _index = faiss.read_index(str(out / "faiss.index"))
    # Load metadata
    _records = json.load(open(out / "records.json"))


@app.get("/search")
def search(q: str, k: int = 5):
    if _model is None or _index is None or _records is None:
        load_index()

    # Encode query
    q_emb = _model.encode([q], convert_to_numpy=True)
    faiss.normalize_L2(q_emb)

    # Search FAISS
    scores, idxs = _index.search(q_emb, k)

    results = []
    for score, idx in zip(scores[0], idxs[0]):
        if idx == -1:
            continue
        rec = _records[idx]
        snippet = rec["text"][:300] + "..." if len(rec["text"]) > 300 else rec["text"]
        results.append({
            "file": rec["file"],
            "chunk_id": rec["chunk_id"],
            "score": float(score),
            "snippet": snippet
        })

    return {"query": q, "results": results}