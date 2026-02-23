import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "7931532868:AAE1JyYv9e_FGlFgwwHwdi5eL0JsmfrLR0k"
GROUP_1_ID = -4996375545
GROUP_2_ID = -5172387855


def clean_message(text):
    money_match = re.search(r"\+?\s*([\d,.]+)\s*(VND|đ)?", text, re.IGNORECASE)
    money = money_match.group(1) if money_match else "?"

    content_match = re.search(r"nội dung[:\s]*(.+)", text, re.IGNORECASE)
    content = content_match.group(1) if content_match else text

    content = re.sub(r"\s+", " ", content).strip()

    return f"💸 {money}đ\n💬 {content}"


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id == GROUP_1_ID:
        text = update.message.text
        result = clean_message(text)
        await context.bot.send_message(chat_id=GROUP_2_ID, text=result)


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()
