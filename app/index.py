# app/index.py
from pathlib import Path
import argparse
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from .ingest.readers import crawl_folder, extract_text_by_ext
from .ingest.chunk import chunk_text


def build_index(root: Path, out: Path = Path("data/index")):
    out.mkdir(parents=True, exist_ok=True)
    files = crawl_folder(root)
    corpus = []
    records = []

    for f in files:
        text = extract_text_by_ext(f)
        for i, ch in enumerate(chunk_text(text)):
            records.append({"file": str(f), "chunk_id": i, "text": ch})
            corpus.append(ch)

    if not corpus:
        print("⚠️ No text found to index.")
        return

    # 🔑 Small Language Model (SLM) for embeddings
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = model.encode(corpus, convert_to_numpy=True, show_progress_bar=True)

    # Normalize embeddings so inner product = cosine similarity
    faiss.normalize_L2(embeddings)

    # Build FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    # Save FAISS index + metadata
    faiss.write_index(index, str(out / "faiss.index"))
    json.dump(records, open(out / "records.json", "w"), ensure_ascii=False)

    print(f"✅ Indexed {len(records)} chunks from {len(files)} files -> {out}")


# ---------------- CLI entry ----------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path, help="Folder to index")
    parser.add_argument("--out", type=Path, default=Path("data/index"), help="Index output directory")
    args = parser.parse_args()
    build_index(args.root, args.out)