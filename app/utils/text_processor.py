import re

def text_sanitizer(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text) 
    text = re.sub(r"\s+", " ", text)    
    text = re.sub(r"[^\w\s.,!?]", "", text) 
    return text.strip()

def chunk_doc(text: str, chunk_size: int = 500, overlap: int = 100) -> list:
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        
        start += chunk_size - overlap

    return chunks
