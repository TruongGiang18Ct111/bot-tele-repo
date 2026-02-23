import telebot
import re

TOKEN = "TOKEN_MOI_CUA_BAN"
GROUP_1_ID = -4996375545
GROUP_2_ID = -5172387855

bot = telebot.TeleBot(TOKEN)


def clean_message(text):
    money_match = re.search(r"\+?\s*([\d,.]+)\s*(VND|đ)?", text, re.IGNORECASE)
    money = money_match.group(1) if money_match else "?"

    content_match = re.search(r"nội dung[:\s]*(.+)", text, re.IGNORECASE)
    content = content_match.group(1) if content_match else text

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


@bot.message_handler(func=lambda message: True)
def handle(message):
    if message.chat.id ==
