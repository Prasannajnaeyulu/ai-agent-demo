# vector_store.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
from config import EMBEDDING_MODEL, FAISS_INDEX_PATH

model = SentenceTransformer(EMBEDDING_MODEL)
index = faiss.IndexFlatL2(384)

def build_index(docs):
    embeddings = model.encode(docs)
    index.add(np.array(embeddings).astype("float32"))
    return docs

def query_index(query, docs, k=3):
    embedding = model.encode([query]).astype("float32")
    D, I = index.search(embedding, k)
    return [docs[i] for i in I[0]]
