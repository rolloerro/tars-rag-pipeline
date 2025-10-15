# rag_pipeline.py
import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer

class RAGSearch:
    def __init__(self, index_path="data/embeddings/faiss.index", docs_path="data/embeddings/docs.pkl"):
        self.index_path = index_path
        self.docs_path = docs_path

        # Загружаем индекс FAISS
        if not os.path.exists(self.index_path):
            raise FileNotFoundError(f"Индекс не найден: {self.index_path}")
        self.index = faiss.read_index(self.index_path)

        # Загружаем документы
        if not os.path.exists(self.docs_path):
            raise FileNotFoundError(f"Документы не найдены: {self.docs_path}")
        with open(self.docs_path, "rb") as f:
            self.documents = pickle.load(f)

        # Загружаем модель для эмбеддингов
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def query(self, question, k=3):
        # Преобразуем вопрос в эмбеддинг
        q_vec = self.model.encode([question])
        D, I = self.index.search(q_vec, k)  # Ищем k ближайших

        results = []
        for idx in I[0]:
            results.append(self.documents[idx])
        return "\n\n".join(results)
