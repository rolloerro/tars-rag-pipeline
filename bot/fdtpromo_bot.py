# fdtpromo_bot.py
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from rag.rag_pipeline import RAGSearch

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Инициализация RAG
rag = RAGSearch()

TOKEN = "8281851943:AAHiQp69U4iMKmQ9OZjEcOuCm9JsoNSTRCo"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Задай вопрос по ФДТ, и я дам ответ из наших документов.")

# Обработка текстовых сообщений
async def answer_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    response = rag.query(question)  # RAG возвращает ответ
    await update.message.reply_text(response)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer_question))
    
    print("Бот запущен! 🚀")
    app.run_polling()

