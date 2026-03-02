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

# --- CONFIG ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

logging.basicConfig(level=logging.INFO)
client = Groq(api_key=GROQ_API_KEY)

# Senior QA Ma'lumotlar Bazasi (Templates)
QA_KNOWLEDGE = {
    "api": "🚀 **API Testing (Postman/Curl)**\n- **Endpoint:** `GET /api/v1/resource`\n- **Headers:** `Content-Type: application/json`\n- **Status Codes:** 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 500 (Server Error)\n- **Checklist:** Response body structure, Data types, Error messages.",
    "sql": "💾 **SQL for QA (Quick Commands)**\n- `SELECT * FROM users WHERE email = 'test@example.com';`\n- `UPDATE orders SET status = 'shipped' WHERE id = 101;`\n- `DELETE FROM logs WHERE created_at < '2023-01-01';` \n- **Tip:** Har doim `SELECT` bilan tekshirib ko'rib, keyin `UPDATE` qil!",
    "severity": "📊 **Severity vs Priority**\n- **S1 (Blocker):** Tizim butunlay ishlamayapti.\n- **S2 (Critical):** Asosiy funksiya buzuq, workaround yo'q.\n- **S3 (Major):** Funksiya xato ishlayapti, lekin workaround bor.\n- **P1 (High):** Darhol tuzatilishi kerak.",
}

SYSTEM_PROMPT = """Siz 20 yillik tajribaga ega Senior QA Engineersiz. 
Junior QA-ga mentorlik qilasiz. Javoblaringiz qisqa, professional va ISTQB standartlariga mos bo'lsin.
Foydalanuvchi qaysi tilda yozsa, o'sha tilda javob bering."""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📝 Checklist", "🧪 Test Case"],
        ["🐞 Bug Report", "🚀 API Testing"],
        ["📊 Severity/Priority", "💾 SQL for QA"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Xush kelibsiz, hamkasb! 🤝 Men sizning Senior QA mentorizman.\n"
        "Loyihangizda qanday yordam kerak? Quyidagilardan birini tanlang:",
        reply_markup=reply_markup,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Static logic
    if text == "🚀 API Testing":
        await update.message.reply_text(QA_KNOWLEDGE["api"])
        return
    elif text == "💾 SQL for QA":
        await update.message.reply_text(QA_KNOWLEDGE["sql"])
        return
    elif text == "📊 Severity/Priority":
        await update.message.reply_text(QA_KNOWLEDGE["severity"])
        return
    # Oldingi shablonlar (Checklist, Test Case, Bug Report) AI orqali yoki static davom etadi

    # AI Logic for anything else
    try:
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            temperature=0.3,
        )
        await update.message.reply_text(response.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(
            "Texnik nosozlik. Senior QA choy ichgani ketdi, birozdan keyin qaytadi."
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()


if __name__ == "__main__":
    main()
