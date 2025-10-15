import os
import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
from PyPDF2 import PdfReader

PDF_FOLDER = Path.home() / "Desktop" / "001.PDF onco"
EMBEDDINGS_DIR = Path("data/embeddings")
EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

docs = []
for pdf_file in PDF_FOLDER.glob("*.pdf"):
    reader = PdfReader(str(pdf_file))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    docs.append(text)

embeddings = model.encode(docs, show_progress_bar=True, convert_to_numpy=True)

dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

faiss.write_index(index, str(EMBEDDINGS_DIR / "faiss.index"))
with open(EMBEDDINGS_DIR / "docs.pkl", "wb") as f:
    pickle.dump(docs, f)

print("✅ Индекс и документы успешно сохранены в", EMBEDDINGS_DIR)
