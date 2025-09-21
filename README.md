# SLM File Searcher

A lightweight local search engine powered by a **Small Language Model (SLM)**.  
Runs **entirely on your machine** — no APIs, no cloud costs — and finds documents by **meaning**, not just keywords.

---

## Features
- **Semantic search**: query “financial institution” → matches files about “banks”.
- **Runs locally**: no API calls, no internet required.
- **Compact**: uses [MiniLM](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) (22M params).
- **File support**: text (`.txt`, `.md`), easily extensible to `.pdf`, `.docx`, `.csv`, `.xlsx`.

---

## Quickstart (macOS / Linux with fish shell)

### 1. Clone the repo
```fish
git clone https://github.com/khal1dkh0n/slm-file-searcher.git

cd slm-file-searcher
```

### 2. Create & Activate virtual environment

```bash
python3 -m venv .venv

source .venv/bin/activate.fish
```

### 3. Install dependencies

```fish
pip install --upgrade pip setuptools wheel

pip install -r requirements.txt
```

### 4. Run the demo

```bash
./demo.fish
```

This will:
1.	Build the index from the current folder
2.	Start the API in the background
3.	Run a test query (emv)
4.	Shut down the API automatically

Example response:
```json
{
  "query": "emv",
  "results": [
    {
      "file": "sample.txt",
      "chunk_id": 0,
      "score": 0.58,
      "snippet": "This is a test document about EMV field 55"
    }
  ]
}
```

## Manual workflow

### If you prefer step by step:

```bash
# 1. Build the index
python3 -m app.index --root .

# 2. Start the API
uvicorn app.api:app --reload

# 3. Search for a keyword
curl "http://127.0.0.1:8000/search?q=emv&k=5"
```

## Repo Structure

```bash
slm-file-searcher/
  ├── app/                # Source code
  │   ├── api.py          # FastAPI server
  │   ├── index.py        # Build FAISS index with embeddings
  │   ├── search.py       # Stub (not used in SLM mode)
  │   └── ingest/         # File reading & chunking
  │       ├── chunk.py
  │       └── readers.py
  │
  ├── data/               # Generated indexes (ignored in .gitignore)
  │   └── index/
  │       ├── faiss.index
  │       └── records.json
  │
  ├── demo.fish           # One-command demo script
  ├── sample.txt          # Example file for testing
  ├── requirements.txt    # Dependencies
  ├── README.md           # This file
  └── .gitignore
```

## Related Post
	•	The Future of AI is Boring — and That’s a Good Thing (Part II)

## License

```
MIT License

Copyright (c) 2025 Khalid Khan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
