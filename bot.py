import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# ==== THAY TOKEN VÀO ĐÂY ====
TOKEN = "7931532868:AAE1JyYv9e_FGlFgwwHwdi5eL0JsmfrLR0k"  # Ví dụ: "7931xxxx:AAExxxxxxx"
GROUP_1_ID = -5172387855    # Group gửi tin nhắn
GROUP_2_ID = -4996375545    # Group nhận tin nhắn

# ==== HÀM LỌC NỘI DUNG ====
def clean_message(text: str) -> str:
    # Lấy số tiền (ví dụ: +5,000 VND)
    money_match = re.search(r"\+?\s*([\d,.]+)\s*(VND|đ)?", text, re.IGNORECASE)
    money = money_match.group(1) if money_match else "?"

    # Lấy phần sau chữ "nội dung"
    content_match = re.search(r"nội dung[:\s]*(.+)", text, re.IGNORECASE)
    content = content_match.group(1) if content_match else text

    # Xóa các pattern rác ngân hàng
    junk_patterns = [
        r"Q[A-Z0-9]+",
        r"APPMB\d*",
        r"Trace\s*\d+",
        r"Ma\s*GD.*",
        r"MBVCB.*",
        r"CT\s*tu.*",
        r"VQR.*",
        r"Chuyen tien.*",
        r"\b\d{6,}\b"
    ]
    for pattern in junk_patterns:
        content = re.sub(pattern, "", content, flags=re.IGNORECASE)

    content = re.sub(r"\s+", " ", content).strip()
    return f"💸 {money}đ\n💬 {content}"

# ==== HÀM XỬ LÝ TIN NHẮN ====
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        print("⚠️ Không có message!")
        return

    # In log tin nhắn nhận được (debug)
    print("Tin nhắn nhận được:", update.message.text)

    # Kiểm tra chat ID đúng group
    if update.effective_chat.id == GROUP_1_ID:
        text = update.message.text
        result = clean_message(text)
        await context.bot.send_message(chat_id=GROUP_2_ID, text=result)
        print("✅ Đã gửi sang GROUP_2")

# ==== BUILD BOT ====
app = ApplicationBuilder().token(TOKEN).build()

# Handler nhận mọi tin nhắn text (bỏ ~filters.COMMAND để đảm bảo nhận cả tin có dấu +)
app.add_handler(MessageHandler(filters.TEXT, handle))

# Chạy bot
app.run_polling()
