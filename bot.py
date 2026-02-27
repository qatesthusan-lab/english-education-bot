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

# ==============================
# ENVIRONMENT
# ==============================
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi!")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY topilmadi!")

client = Groq(api_key=GROQ_API_KEY)

logging.basicConfig(level=logging.INFO)

# ==============================
# 1️⃣ MAIN SYSTEM PROMPT
# ==============================
MAIN_PROMPT = """
Sen professional English mentor va aqlli suhbatdoshsan.

QOIDALAR:
- Asosan o‘zbek tilida tushuntir.
- Inglizcha misol bersang, izohini o‘zbekcha qil.
- Turk tilidan foydalanma.
- Foydalanuvchi savolini tarjima qilib qaytarma.
- Qisqa, aniq va mantiqli yoz.
"""

# ==============================
# 2️⃣ GRAMMAR FIX PROMPT
# ==============================
GRAMMAR_FIX_PROMPT = """
Quyidagi matnni adabiy va grammatik jihatdan to‘g‘ri O‘ZBEK tiliga tuzat.
Mazmunni o‘zgartirma.
Keraksiz ro‘yxat va sun’iy iboralarni olib tashla.
Faqat tozalangan matnni qaytar.
"""


# ==============================
# START
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom 👋\n\n"
        "Men professional English mentor va aqlli suhbatdoshman.\n"
        "Savol bering yoki gaplashamiz 🤖"
    )


# ==============================
# MESSAGE HANDLER
# ==============================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        # 1️⃣ STEP — AI javob yaratadi
        first_response = await asyncio.to_thread(
            client.chat.completions.create,
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": MAIN_PROMPT},
                {"role": "user", "content": user_text},
            ],
            temperature=0.4,
        )

        raw_reply = first_response.choices[0].message.content

        # 2️⃣ STEP — O‘zbek grammatik tuzatish
        fixed_response = await asyncio.to_thread(
            client.chat.completions.create,
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": GRAMMAR_FIX_PROMPT},
                {"role": "user", "content": raw_reply},
            ],
            temperature=0.2,
        )

        final_reply = fixed_response.choices[0].message.content

        await update.message.reply_text(final_reply[:4000])

    except Exception as e:
        await update.message.reply_text(f"Xatolik:\n{e}")


# ==============================
# MAIN
# ==============================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 2-Bosqichli AI Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
