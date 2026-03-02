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

# --- SIZNING TOKENLARINGIZ ---
BOT_TOKEN = "BOT_TOKEN"
GROQ_API_KEY = "GROQ_API_KEY"

# Groq mijozini sozlash
client = Groq(api_key=GROQ_API_KEY)
logging.basicConfig(level=logging.INFO)

# QA Mutaxassisi uchun Professional Prompt
SYSTEM_PROMPT = """Siz professional Senior QA Automation Engineer va Manual Testerisiz. 
Vazifangiz: Checklist, Test Case va Bug Report tayyorlashda yordam berish.

QA STANDARTLARI:
1. Test Case yozganda: ID, Title, Pre-conditions, Steps, Expected Result formatida yozing.
2. Bug Report yozganda: Summary, Steps to Reproduce, Expected vs Actual Result, Severity bo'lsin.
3. Checklist yozganda: Mantiqiy guruhlangan (UI, Functional, Performance) qismlarga bo'ling.

TIL QOIDASI:
Foydalanuvchi qaysi tilda yozsa, JAVOBNI FAQAT O‘SHA TILDA BER.
Hech qachon boshqa tilga o‘tma. Professional terminologiyadan foydalaning.
"""

MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
user_memory = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Siz so'ragan menu tugmalari
    keyboard = [["📝 Checklist", "🧪 Test Case"], ["🐞 Bug Report"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Salom! Men sizning professional QA yordamchingizman. 🛡️\n"
        "Quyidagi tugmalardan birini tanlang yoki loyihangiz haqida yozing:",
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
            continue
    raise last_error


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    # Tugmalarga mos mantiqiy kontekst
    if user_text == "📝 Checklist":
        prompt_context = "Loyiha uchun professional QA checklist shablonini taqdim et."
    elif user_text == "🧪 Test Case":
        prompt_context = "Menga test case yozishda yordam ber. Format: ID, Title, Steps, Expected Result."
    elif user_text == "🐞 Bug Report":
        prompt_context = "Professional Bug Report qanday yoziladi? Misol keltir."
    else:
        prompt_context = user_text

    if user_id not in user_memory:
        user_memory[user_id] = []

    user_memory[user_id].append({"role": "user", "content": prompt_context})
    user_memory[user_id] = user_memory[user_id][-8:]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += user_memory[user_id]

    try:
        reply = await generate_response(messages)
        user_memory[user_id].append({"role": "assistant", "content": reply})
        await update.message.reply_text(reply, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"Xatolik yuz berdi: {e}")


def main():
    # Botni ishga tushirish
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 QA Professional AI Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
