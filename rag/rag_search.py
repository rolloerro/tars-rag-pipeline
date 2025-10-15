#!/usr/bin/env python3
"""
Поиск по векторной базе с помощью FAISS + SentenceTransformer.
"""

import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Загружаем
index = faiss.read_index("data/embeddings/faiss.index")
with open("data/embeddings/docs.pkl", "rb") as f:
    documents = pickle.load(f)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Запрос пользователя
query = input("🔍 Введите вопрос: ")

# Кодируем и ищем
query_emb = model.encode([query])
distances, indices = index.search(query_emb, k=2)

print("\n🔎 Результаты поиска:")
for i, idx in enumerate(indices[0]):
    print(f"{i+1}. {documents[idx]} (distance={distances[0][i]:.4f})")
