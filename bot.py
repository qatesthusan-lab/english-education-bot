import os
import logging
import asyncio
from groq import Groq
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# --- KONFIGURATSIYA ---
# Railway Variables bo'limidan olinadi
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Groq klientini ishga tushirish
client = Groq(api_key=GROQ_API_KEY)

# QA Professional Prompt
SYSTEM_PROMPT = """Siz professional Senior QA Engineer va Manual Testerisiz. 
Vazifangiz: Checklist, Test Case va Bug Report tayyorlashda yordam berish.

QA STANDARTLARI:
1. Test Case: ID, Title, Pre-conditions, Steps, Expected Result.
2. Bug Report: Summary, Steps to Reproduce, Expected vs Actual Result, Severity.
3. UI Testing: Vizual elementlar, responsive dizayn va UXga e'tibor bering.

MUHIM: Foydalanuvchi qaysi tilda yozsa, faqat o'sha tilda javob bering. 
Javoblarni aniq va tushunarli formatda chiqaring."""

MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
user_memory = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Asosiy menu tugmalari
    keyboard = [["📝 Checklist", "🧪 Test Case"], ["🐞 Bug Report"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Salom! Men sizning professional QA yordamchingizman. 🛡️\n"
        "Quyidagi tugmalardan birini tanlang yoki savolingizni yozing:",
        reply_markup=reply_markup,
    )


async def generate_response(messages):
    last_error = None
    for model in MODELS:
        try:
            response = await asyncio.to_thread(
                client.chat.completions.create,
                model=model,
                messages=messages,
                temperature=0.4,
            )
            return response.choices[0].message.content
        except Exception as e:
            last_error = e
            logger.error(f"Model {model} xatosi: {e}")
            continue
    raise last_error


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    # Tugmalar uchun maxsus kontekst
    if user_text == "📝 Checklist":
        user_query = "QA uchun checklist shablonini ber yoki tuzishga yordam ber."
    elif user_text == "🧪 Test Case":
        user_query = "Menga professional Test Case yozishda yordam ber."
    elif user_text == "🐞 Bug Report":
        user_query = "Bug Report qanday yoziladi? Professional formatda tushuntir."
    else:
        user_query = user_text

    # Xotirani tekshirish
    if user_id not in user_memory:
        user_memory[user_id] = []

    user_memory[user_id].append({"role": "user", "content": user_query})
    user_memory[user_id] = user_memory[user_id][-8:]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += user_memory[user_id]

    try:
        reply = await generate_response(messages)
        user_memory[user_id].append({"role": "assistant", "content": reply})

        # Markdown xatosini oldini olish uchun parse_mode ishlatmaymiz
        await update.message.reply_text(reply)

    except Exception as e:
        logger.error(f"Xabar yuborishda xatolik: {e}")
        await update.message.reply_text(
            "Kechirasiz, xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
        )


def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN topilmadi!")
        return

    # Application qurish
    application = Application.builder().token(BOT_TOKEN).build()

    # Handlerlarni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    # Botni ishga tushirish
    print("🚀 QA Professional AI Bot Railway serverida ishlamoqda...")
    application.run_polling()


if __name__ == "__main__":
    main()
