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
=======
import pickle
from sentence_transformers import SentenceTransformer
import faiss

index_path = "data/embeddings/faiss.index"
docs_path = "data/embeddings/docs.pkl"

with open(docs_path, "rb") as f:
    docs = pickle.load(f)

index = faiss.read_index(index_path)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def search(query, top_k=3):
    query_vec = model.encode([query])
    D, I = index.search(query_vec, top_k)
    results = [docs[i] for i in I[0]]
    return results

def generate_answer(query):
    results = search(query)
    answer = "\n---\n".join(results)
    return answer

if __name__ == "__main__":
    query = input("Введите вопрос: ")
    answer = generate_answer(query)
    print("\n🔍 Результат поиска + генерации:\n", answer)
>>>>>>> 303a71b (🚀 Начальный RAG MVP с PDF поиском и генерацией ответов)
