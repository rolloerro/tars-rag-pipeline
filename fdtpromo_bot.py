# fdtpromo_bot.py
import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from rag.rag_pipeline import RAGSearch

# Загружаем .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Инициализация RAG
rag = RAGSearch()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Задай вопрос по ФДТ, и я найду ответ в документах.")

# Обработка текста
async def answer_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    response = rag.query(question)
    # ограничим ответ 500 символами
    for chunk in [response[i:i+500] for i in range(0, len(response), 500)]:
        await update.message.reply_text(chunk)

if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("❌ Не найден BOT_TOKEN в .env")
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer_question))

    print("Бот запущен! 🚀")
    app.run_polling()
