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
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = Groq(api_key=GROQ_API_KEY)

# Professional QA Shablonlari
TEMPLATES = {
    "checklist": """📝 **QA CHECKLIST SHABLONI**
---
1. **UI/UX Tekshiruvi:**
   - [ ] Barcha tugmalar bosiladimi?
   - [ ] Ranglar va shriftlar dizaynga mosmi?
   - [ ] Adaptivlik (Mobile/Tablet) joyidami?
2. **Funksionallik:**
   - [ ] Login/Register to'g'ri ishlayaptimi?
   - [ ] Validatsiyalar (bo'sh maydon, xato format) ishlayaptimi?
   - [ ] Ma'lumotlar bazasiga to'g'ri saqlanyaptimi?
3. **Performance:**
   - [ ] Sahifa 3 soniyadan tez yuklanyaptimi?
""",
    "testcase": """🧪 **TEST CASE SHABLONI**
---
**ID:** TC-001
**Title:** [Tizim nomi] - [Funksiya nomi]ni tekshirish
**Pre-conditions:** Foydalanuvchi tizimga kirgan bo'lishi kerak.
**Steps:**
1. Sahifaga o'ting.
2. [X] tugmasini bosing.
3. Ma'lumotlarni kiriting.
**Expected Result:** Tizim "Muvaffaqiyatli" xabarini chiqarishi kerak.
**Priority:** High/Medium/Low
""",
    "bugreport": """🐞 **BUG REPORT SHABLONI**
---
**Summary:** [Qisqa va aniq sarlavha]
**Severity:** Critical / Major / Minor
**Priority:** High / Medium / Low
**Steps to Reproduce:**
1. Ilovani oching.
2. Menyuga kiring.
3. [X] tugmasini bosing.
**Actual Result:** Tizim xatolik berib yopilib qoldi.
**Expected Result:** Tugma bosilganda keyingi sahifa ochilishi kerak.
**Environment:** Chrome v120, Windows 11.
""",
}

SYSTEM_PROMPT = "Siz Senior QA muhandisisiz. Foydalanuvchi qaysi tilda yozsa, faqat o'sha tilda javob bering."


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📝 Checklist", "🧪 Test Case"], ["🐞 Bug Report"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Salom! Men professional QA yordamchiman. Quyidagi tugmalar orqali tayyor shablonlarni olishingiz yoki AI dan so'rashingiz mumkin:",
        reply_markup=reply_markup,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # 1. Shablonlarni tekshirish
    if user_text == "📝 Checklist":
        await update.message.reply_text(TEMPLATES["checklist"])
        return
    elif user_text == "🧪 Test Case":
        await update.message.reply_text(TEMPLATES["testcase"])
        return
    elif user_text == "🐞 Bug Report":
        await update.message.reply_text(TEMPLATES["bugreport"])
        return

    # 2. Agar tugma emas, savol bo'lsa AI javob beradi
    try:
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
            temperature=0.4,
        )
        await update.message.reply_text(response.choices[0].message.content)
    except Exception as e:
        logger.error(f"Xato: {e}")
        await update.message.reply_text(
            "Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🚀 Bot Railway serverida ishlamoqda...")
    app.run_polling()


if __name__ == "__main__":
    main()
