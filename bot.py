import logging
import random
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    await update.message.reply_text(
        "🎓 Welcome to English Education Bot!", reply_markup=keyboard
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if text == "📘 grammar".lower():
        lesson_text = ""
        for key, value in grammar_lessons.items():
            lesson_text += f"\n🔹 {key.title()}:\n{value}\n"
        await update.message.reply_text(lesson_text)

    elif text == "📝 ielts quiz".lower():
        q = random.choice(ielts_questions)
        context.user_data["answer"] = q["answer"]
        options = "\n".join(q["options"])
        await update.message.reply_text(f"{q['question']}\n\n{options}")

    elif "answer" in context.user_data:
        if text == context.user_data["answer"]:
            await update.message.reply_text("✅ Correct!")
        else:
            await update.message.reply_text("❌ Wrong answer.")
        context.user_data.pop("answer")

    elif text == "🎯 cefr test".lower():
        await update.message.reply_text("Translate: 'Men maktabga bordim'")
        context.user_data["cefr"] = True

    elif "cefr" in context.user_data:
        if "i went to school" in text:
            await update.message.reply_text("✅ Level: A2")
        else:
            await update.message.reply_text("⚠️ Try: I went to school")
        context.user_data.pop("cefr")

    else:
        await update.message.reply_text("Use menu buttons.")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot ishlayapti...")
    app.run_polling()


if __name__ == "__main__":
    main()
