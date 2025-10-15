import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from sentence_transformers import SentenceTransformer, util
from PyPDF2 import PdfReader
from dotenv import load_dotenv  # pip install python-dotenv

# Загружаем переменные из .env
load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Путь к PDF
PDF_PATH = os.path.expanduser("~/Desktop/001_onco.pdf")

# Загружаем PDF
def load_pdf(path):
    reader = PdfReader(path)
    sentences = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            sentences.extend(text.split('. '))
    return sentences

sentences = load_pdf(PDF_PATH)

# Модель для поиска по смыслу
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
sentence_embeddings = model.encode(sentences, convert_to_tensor=True)

# Функция ответа
async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    query_embedding = model.encode(query, convert_to_tensor=True)
    hits = util.semantic_search(query_embedding, sentence_embeddings, top_k=1)
    result = sentences[hits[0][0]['corpus_id']]
    await update.message.reply_text(result[:300])  # Ограничиваем 300 символами

# Создаем приложение бота
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))

print("Бот запущен! 🚀")
app.run_polling()
