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
# ENV
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
# START
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "Salom 👋\n\n" "Menga inglizcha savol yozing — AI javob beradi 🤖"
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
            model="llama-3.1-8b-instant",  # Hozir ishlaydigan model
            messages=[
                {"role": "system", "content": "You are a helpful English teacher."},
                {"role": "user", "content": user_text},
            ],
        )

        reply = response.choices[0].message.content

        if reply:
            await update.message.reply_text(reply[:4000])
        else:
            await update.message.reply_text("AI javob bera olmadi.")

    except Exception as e:
        await update.message.reply_text(f"Error:\n{e}")


# ==============================
# MAIN
# ==============================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
