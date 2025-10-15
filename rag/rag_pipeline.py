from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# 1. Загружаем эмбеддинг-модель
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Наши документы (демо)
docs = [
    "ML Engineer designs models for real-world applications.",
    "RAG combines retrieval with generation to enhance LLM accuracy.",
    "Vector databases store embeddings for semantic search.",
]

# 3. Создаём эмбеддинги
embeddings = model.encode(docs)
embeddings = np.array(embeddings).astype('float32')

# 4. Индексируем с помощью FAISS
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# 5. Поисковый запрос
query = "How does RAG improve LLMs?"
query_emb = model.encode([query]).astype('float32')

# 6. Поиск ближайшего документа
_, indices = index.search(query_emb, k=1)
print("🔍 Best match:", docs[indices[0][0]])
