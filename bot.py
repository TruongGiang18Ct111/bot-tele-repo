from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "7931532868:AAE1JyYv9e_FGlFgwwHwdi5eL0JsmfrLR0k"

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        print("⚠️ Không có message!")
    else:
        print("Tin nhắn nhận được từ chat_id =", update.effective_chat.id)
        print("Nội dung:", update.message.text)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))
app.run_polling()
