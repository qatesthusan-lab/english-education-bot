import os
import logging
import asyncio
from groq import Groq
from jira import JIRA
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# --- KONFIGURATSIYA (Railway Variables) ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "MFT")

# Logging - Muammolarni kuzatish uchun
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Klientlarni ishga tushirish
client = Groq(api_key=GROQ_API_KEY)


def get_jira_client():
    # URL-ni tozalash: https://name.atlassian.net ko'rinishiga keltirish
    base_url = JIRA_URL.split('/jira/')[0] if '/jira/' in JIRA_URL else JIRA_URL
    return JIRA(server=base_url, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))


# Senior QA Prompt
SYSTEM_PROMPT = """Siz 20 yillik tajribaga ega Senior QA Lead muhandisiz. 
Vazifangiz: Foydalanuvchi yozgan xabarni professional Jira formatiga (Summary, Steps to Reproduce, Expected/Actual Result) keltirish. 
Faqat tanlangan tilda javob bering."""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📝 Checklist & Test Case", "🐞 Bug Report"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Xush kelibsiz, Senior QA! 🤜🤛\nJira (MFT) integratsiyasi tayyor.\n"
        "Muammoni yoki test rejani yozing, men uni professional hisobot qilaman.",
        reply_markup=reply_markup,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['raw_input'] = update.message.text

    keyboard = [
        [
            InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data='uz_lang'),
            InlineKeyboardButton("🇷🇺 Русский", callback_data='ru_lang'),
            InlineKeyboardButton("🇺🇸 English", callback_data='en_lang'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hisobot qaysi tilda tayyorlansin?", reply_markup=reply_markup
    )


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    lang_map = {'uz_lang': 'O\'zbek tili', 'ru_lang': 'Rus tili', 'en_lang': 'English'}

    if data not in lang_map:
        return

    selected_lang = lang_map[data]
    raw_text = context.user_data.get('raw_input')

    await query.edit_message_text(
        text=f"🔄 AI {selected_lang}da professional hisobot tayyorlamoqda..."
    )

    try:
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"{SYSTEM_PROMPT} Javobni faqat {selected_lang}da yozing.",
                },
                {"role": "user", "content": raw_text},
            ],
            temperature=0.3,
        )
        report = response.choices[0].message.content
        context.user_data['last_report'] = report

        keyboard = [
            [
                InlineKeyboardButton(
                    "🚀 Jira'ga yuborish (MFT)", callback_data='send_to_jira'
                )
            ]
        ]
        await query.edit_message_text(
            text=f"📋 **Tayyorlangan Hisobot ({selected_lang}):**\n\n{report}",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    except Exception as e:
        logger.error(f"AI Error: {e}")
        await query.message.reply_text(
            f"❌ AI Xatosi (API Key-ni tekshiring): {str(e)}"
        )


async def jira_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    report_content = context.user_data.get('last_report')
    if not report_content:
        await query.message.reply_text("Xatolik: Hisobot topilmadi.")
        return

    await query.edit_message_text(text="⏳ Jira'ga yuborilmoqda...")

    try:
        jira = get_jira_client()
        # Summary (Sarlavha) tayyorlash
        summary = (
            report_content.split('\n')[0][:100]
            .replace('#', '')
            .replace('*', '')
            .strip()
        )

        issue_dict = {
            'project': PROJECT_KEY,  # 'MFT' kodi Railway Variables-dan keladi
            'summary': summary or "Bug Report from Telegram",
            'description': report_content,
            'issuetype': {'name': 'Bug'},
        }

        new_issue = await asyncio.to_thread(jira.create_issue, fields=issue_dict)

        await query.edit_message_text(
            text=f"✅ **JIRA TICKET OCHILDI!**\n\n🆔 ID: `{new_issue.key}`\n🔗 [Ticketni ko'rish]({new_issue.permalink()})",
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.error(f"Jira Error: {e}")
        await query.message.reply_text(
            f"❌ Jira xatosi: {str(e)}\n\nLoyiha kodi: {PROJECT_KEY}"
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        CallbackQueryHandler(language_callback, pattern='^(uz_lang|ru_lang|en_lang)$')
    )
    app.add_handler(CallbackQueryHandler(jira_callback, pattern='^send_to_jira$'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Senior QA Bot ishga tushdi...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
