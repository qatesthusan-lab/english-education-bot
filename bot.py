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

# ==============================
# GROQ CLIENT
# ==============================
client = Groq(api_key=GROQ_API_KEY)

# ==============================
# LOGGING
# ==============================
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ==============================
# PROFESSIONAL SYSTEM PROMPT
# ==============================
SYSTEM_PROMPT = """
Sen professional English mentor va aqlli suhbatdoshsan.

SENING VAZIFANG:
- Ingliz tilini professional darajada o‘rgatish
- Oddiy va tushunarli qilib tushuntirish
- Do‘stona, lekin professional ohangda gapirish
- Kerak bo‘lsa misollar berish
- Grammatikani sodda qilib tushuntirish
- Foydalanuvchining saviyasiga moslashish

QOIDALAR:
- Asosan O‘ZBEK tilida tushuntir.
- Agar misol kerak bo‘lsa inglizcha misol ber, lekin izohini o‘zbekcha qil.
- Hech qachon turk tilida yozma.
- Foydalanuvchi savolini tarjima qilib qaytarma.
- Agar oddiy suhbat bo‘lsa, tabiiy va aqlli suhbatdosh kabi javob ber.
- Juda uzun va zerikarli yozma.
- Aniq, strukturali va tushunarli yoz.

Agar foydalanuvchi shunchaki gaplashmoqchi bo‘lsa —
aqlli, qiziqarli suhbat olib bor.

Agar u grammar yoki IELTS haqida so‘rasa —
professional teacher rejimiga o‘t.
"""


# ==============================
# START
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "Salom 👋\n\n"
            "Men sizning English mentor va aqlli suhbatdoshingizman.\n"
            "Savol bering yoki shunchaki gaplashamiz 🤖"
        )


# ==============================
# MESSAGE HANDLER
# ==============================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_text = update.message.text

    try:
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
            temperature=0.7,
        )

        reply = response.choices[0].message.content

        if reply:
            await update.message.reply_text(reply[:4000])
        else:
            await update.message.reply_text("AI javob bera olmadi.")

    except Exception as e:
        await update.message.reply_text(f"Xatolik:\n{e}")


# ==============================
# MAIN
# ==============================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Professional AI Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
