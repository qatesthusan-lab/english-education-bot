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

# Har user uchun memory
user_memory = {}

SYSTEM_PROMPT = """SYSTEM_PROMPT = 
Sen yuqori darajadagi aqlli AI assistant va professional English mentorsan.

ENG MUHIM QOIDA:
Foydalanuvchi qaysi tilda yozsa, JAVOBNI FAQAT O‘SHA TILDA BER.

- Agar foydalanuvchi o‘zbek tilida yozsa → o‘zbek tilida javob ber,agar rus tilida yozsa → rus tilida javob ber,agar kores tilida yozsa → koreys tilida javob ber
- Agar ingliz tilida yozsa → ingliz tilida javob ber.
- Hech qachon boshqa tilga o‘tma.
- Foydalanuvchi matnini tarjima qilib qaytarma.
- Turk tilidan foydalanma.
va sen matematika va ingliz tili bo‘yicha professional o‘qituvchisan, shuning uchun har doim foydalanuvchining savollariga batafsil va tushunarli javob ber, kerak bo‘lsa misollar keltir. hamda mental aritmetikani ham tushuntir.metal arifmetika boyicha sen eng professional o‘qituvchisan, shuning uchun har doim foydalanuvchining savollariga batafsil va tushunarli javob ber, kerak bo‘lsa misollar keltir.

Agar ingliz tili haqida savol bo‘lsa → professional teacher kabi tushuntir.
Agar oddiy suhbat bo‘lsa → tabiiy va aqlli suhbat olib bor.

Javoblar ravon, mantiqli va sun’iy bo‘lmasin.
Keraksiz ro‘yxatlar ishlatma.
"""


# Ishlaydigan modellardan ro‘yxat (fallback)
MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom 👋\nMen aqlli AI mentor va suhbatdoshman.\nGaplashamizmi? "
    )


async def generate_response(messages):
    last_error = None
    for model in MODELS:
        try:
            response = await asyncio.to_thread(
                client.chat.completions.create,
                model=model,
                messages=messages,
                temperature=0.5,
            )
            return response.choices[0].message.content
        except Exception as e:
            last_error = e
            continue
    raise last_error


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    if user_id not in user_memory:
        user_memory[user_id] = []

    user_memory[user_id].append({"role": "user", "content": user_text})
    user_memory[user_id] = user_memory[user_id][-8:]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += user_memory[user_id]

    try:
        reply = await generate_response(messages)

        user_memory[user_id].append({"role": "assistant", "content": reply})
        user_memory[user_id] = user_memory[user_id][-8:]

        await update.message.reply_text(reply[:4000])

    except Exception as e:
        await update.message.reply_text(f"Xatolik:\n{e}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Ultimate Smart AI ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
