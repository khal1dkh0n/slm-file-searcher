# app/ingest/chunk.py

def chunk_text(text, size=900, overlap=150):
    chunks=[]
    i=0
    while i < len(text):
        j=min(i+size, len(text))
        chunks.append(text[i:j])
        if j==len(text): break
        i=j-overlap if j-overlap>i else j
    return chunks
