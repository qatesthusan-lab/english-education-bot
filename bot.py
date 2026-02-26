import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("START BOSILDI")
    await update.message.reply_text("Bot ishlayapti!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("XABAR KELDI:", update.message.text)
    await update.message.reply_text("Siz yozdingiz: " + (update.message.text or ""))


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot ishga tushdi")
    app.run_polling()


if __name__ == "__main__":
    main()
