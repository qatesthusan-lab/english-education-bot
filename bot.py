import os
import logging
import asyncio
from groq import Groq
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
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
client = Groq(api_key=GROQ_API_KEY)

# Senior Bilimlar Bazasi
QA_KNOWLEDGE = {
    "automation": "🤖 **Automation Roadmap (Junior to Senior)**\n\n"
    "1. **Language:** Python yoki Java asoslarini o'rganing.\n"
    "2. **Locators:** CSS Selectors va XPath (Absolute vs Relative) farqini biling.\n"
    "3. **Frameworks:** Pytest (Python) yoki JUnit/TestNG (Java).\n"
    "4. **Tools:** Selenium, Playwright (Zamonaviy tanlov), Appium (Mobile).\n"
    "5. **CI/CD:** Jenkins yoki GitHub Actions orqali testlarni avtomatik yurgizish.",
    "techniques": "📐 **Test Design Techniques (Kalkulyator)**\n\n"
    "Sizga diapazonni tahlil qilib beraman. Masalan, '1-100 oralig'i' deb yozsangiz, "
    "men sizga Boundary Value Analysis (BVA) nuqtalarini chiqarib beraman.",
}

# Tizim ko'rsatmasi (System Prompt)
SYSTEM_PROMPT = """Siz 20 yillik tajribaga ega Senior QA Lead va SDET muhandisiz. 
Sizning vazifangiz Junior QA muhandisini Senior darajasiga ko'tarishdir.
Javoblaringizda doim:
1. ISTQB terminologiyasidan foydalaning.
2. Loglar yuborilsa, ularni tahlil qilib, 'Root Cause' (Asosiy sabab) ni toping.
3. Avtomatlashtirish bo'yicha eng yaxshi praktikalarni (Page Object Model, DRY, SOLID) tavsiya qiling.
Foydalanuvchi qaysi tilda yozsa, o'sha tilda javob bering."""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📝 Checklist & Test Case", "🐞 Bug Report"],
        ["🏗️ Test Turlari", "🤖 Automation Roadmap"],
        ["📊 Severity/Priority", "📐 Test Techniques"],
        ["🚀 API & SQL Hub", "👨‍🏫 Interview Mentor"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Xush kelibsiz, Senior QA kursiga! ⚔️\n\n"
        "Men sizning shaxsiy mentorizman. Bu yerda biz shunchaki test qilmaymiz, "
        "biz sifatli mahsulot quramiz. Qaysi yo'nalishdan boshlaymiz?",
        reply_markup=reply_markup,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Static Professional Knowledge
    if text == "🤖 Automation Roadmap":
        await update.message.reply_text(QA_KNOWLEDGE["automation"])
        return
    elif text == "📐 Test Techniques":
        await update.message.reply_text(QA_KNOWLEDGE["techniques"])
        return
    elif text == "🚀 API & SQL Hub":
        await update.message.reply_text(
            "Endpointlar, status kodlari yoki SQL querylar bo'yicha nima savolingiz bor?"
        )
        return

    # AI Mentor & Log Analyzer Logic
    try:
        # Junior ko'pincha log tashlaydi, AI uni tahlil qilishi kerak
        is_log = (
            "error" in text.lower()
            or "exception" in text.lower()
            or "stack trace" in text.lower()
        )

        prefix = "🚨 **Log Tahlili:**\n" if is_log else ""

        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            temperature=0.3,
        )
        await update.message.reply_text(prefix + response.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(
            "⚠️ Tizimda kichik bug topildi. Mentor uni tuzatmoqda."
        )


def main():
    if not BOT_TOKEN:
        print("XATO: BOT_TOKEN topilmadi!")
        return

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Senior QA Hub Railway'da ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
