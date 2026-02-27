import os
import logging
import asyncio
from groq import Groq
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi!")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY topilmadi!")

client = Groq(api_key=GROQ_API_KEY)

logging.basicConfig(level=logging.INFO)

# Har user uchun xotira
user_memory = {}

SYSTEM_PROMPT = """
Sen yuqori darajadagi aqlli AI assistant va professional English mentor san.

QOIDALAR:
- Foydalanuvchi qaysi tilda yozsa, o‘sha tilda javob ber.
- Agar ingliz tili haqida savol bo‘lsa, teacher rejimiga o‘t.
- Agar oddiy suhbat bo‘lsa, tabiiy va aqlli suhbatdosh bo‘l.
- Keraksiz ro‘yxatlar va sun’iy punktlardan qoch.
- Juda uzun yozma.
- Aniq va ravon yoz.
- Turk tilidan foydalanma.
- Foydalanuvchi savolini tarjima qilib qaytarma.
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom 👋\nMen aqlli suhbatdosh va English mentor man.\nGaplashamizmi? 😎"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    if user_id not in user_memory:
        user_memory[user_id] = []

    # So‘nggi 6 ta xabarni saqlaymiz
    user_memory[user_id].append({"role": "user", "content": user_text})
    user_memory[user_id] = user_memory[user_id][-6:]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += user_memory[user_id]

    try:
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="llama-3.1-70b-versatile",  # Kuchliroq model
            messages=messages,
            temperature=0.6,
        )

        reply = response.choices[0].message.content

        # AI javobini ham memoryga qo‘shamiz
        user_memory[user_id].append({"role": "assistant", "content": reply})
        user_memory[user_id] = user_memory[user_id][-6:]

        await update.message.reply_text(reply[:4000])

    except Exception as e:
        await update.message.reply_text(f"Xatolik:\n{e}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Smart AI ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
