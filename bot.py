import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("START BOSILDI")
    await update.message.reply_text("Bot ishlayapti!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("XABAR:", update.message.text)
    await update.message.reply_text(f"Siz yozdingiz: {update.message.text}")


async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot ishga tushdi...")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
