import os
import logging
import random
import google.generativeai as genai
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ==============================
# ENV VARIABLES
# ==============================
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ==============================
# GEMINI SETUP
# ==============================
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# ==============================
# LOGGING
# ==============================
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ==============================
# STATIC DATA
# ==============================
grammar_lessons = {
    "present simple": "Present Simple: Daily routines.\nExample: I go to school.",
    "past simple": "Past Simple: Finished actions.\nExample: I went yesterday.",
    "future simple": "Future Simple: Future plans.\nExample: I will go tomorrow.",
}

ielts_questions = [
    {
        "question": "She ___ to school yesterday.",
        "options": ["go", "went", "gone"],
        "answer": "went",
    }
]

main_menu = [["📘 Grammar", "📝 IELTS Quiz"], ["🎯 CEFR Test"]]


# ==============================
# COMMANDS
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    await update.message.reply_text(
        "🎓 Welcome to English Education Bot!\n\n"
        "You can:\n"
        "• Use menu buttons\n"
        "• Or just chat with AI in English 🤖",
        reply_markup=keyboard,
    )


# ==============================
# MESSAGE HANDLER
# ==============================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    # Grammar
    if text == "📘 grammar".lower():
        lesson_text = ""
        for key, value in grammar_lessons.items():
            lesson_text += f"\n🔹 {key.title()}:\n{value}\n"
        await update.message.reply_text(lesson_text)
        return

    # IELTS
    elif text == "📝 ielts quiz".lower():
        q = random.choice(ielts_questions)
        context.user_data["answer"] = q["answer"]
        options = "\n".join(q["options"])
        await update.message.reply_text(f"{q['question']}\n\n{options}")
        return

    # IELTS answer check
    elif "answer" in context.user_data:
        if text == context.user_data["answer"]:
            await update.message.reply_text("✅ Correct!")
        else:
            await update.message.reply_text("❌ Wrong answer.")
        context.user_data.pop("answer")
        return

    # CEFR
    elif text == "🎯 cefr test".lower():
        await update.message.reply_text("Translate: 'Men maktabga bordim'")
        context.user_data["cefr"] = True
        return

    elif "cefr" in context.user_data:
        if "i went to school" in text:
            await update.message.reply_text("✅ Level: A2")
        else:
            await update.message.reply_text("⚠️ Try: I went to school")
        context.user_data.pop("cefr")
        return

    # ==============================
    # AI CHAT (DEFAULT)
    # ==============================
    else:
        try:
            response = model.generate_content(update.message.text)
            await update.message.reply_text(response.text)
        except Exception as e:
            logging.error(e)
            await update.message.reply_text("AI error 😢")


# ==============================
# MAIN
# ==============================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Bot AI bilan ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
