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

# --- KONFIGURATSIYA ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "MFT")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

client = Groq(api_key=GROQ_API_KEY)


def get_jira_client():
    base_url = JIRA_URL.split('/jira/')[0] if '/jira/' in JIRA_URL else JIRA_URL
    return JIRA(server=base_url, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📝 Checklist & Test Case", "🐞 Bug Report"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Salom Senior QA! Muammoni yozing:", reply_markup=reply_markup
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Foydalanuvchi yuborgan matnni saqlaymiz (Xavfsizroq usul)
    user_id = update.effective_user.id
    context.user_data[f'text_{user_id}'] = update.message.text

    keyboard = [
        [
            InlineKeyboardButton("🇺🇿 UZ", callback_data='lang_uz'),
            InlineKeyboardButton("🇷🇺 RU", callback_data='lang_ru'),
            InlineKeyboardButton("🇺🇸 EN", callback_data='lang_en'),
        ]
    ]
    await update.message.reply_text(
        "Tilni tanlang:", reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Tugma aylanishini darhol to'xtatamiz

    user_id = update.effective_user.id
    raw_text = context.user_data.get(f'text_{user_id}')

    if not raw_text:
        await query.edit_message_text("❌ Matn topilmadi, iltimos qaytadan yozing.")
        return

    lang_code = query.data.split('_')[1]
    lang_name = {'uz': 'O\'zbek tili', 'ru': 'Rus tili', 'en': 'English'}[lang_code]

    await query.edit_message_text(f"⏳ AI {lang_name}da tayyorlamoqda...")

    try:
        # AI so'rovini bloklamaydigan holda bajarish
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"Senior QA. Jira format. Language: {lang_name}",
                },
                {"role": "user", "content": raw_text},
            ],
            temperature=0.3,
        )
        report = response.choices[0].message.content
        context.user_data[f'report_{user_id}'] = report

        keyboard = [
            [InlineKeyboardButton("🚀 Jira'ga yuborish", callback_data='to_jira')]
        ]
        await query.edit_message_text(
            f"📋 **Hisobot:**\n\n{report}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.error(f"AI Error: {e}")
        await query.message.reply_text(f"❌ AI xatosi yuz berdi.")


async def jira_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    report = context.user_data.get(f'report_{user_id}')

    if not report:
        await query.message.reply_text("❌ Hisobot yo'qolgan.")
        return

    await query.edit_message_text("⏳ Jira'ga yuborilmoqda...")

    try:
        jira = get_jira_client()
        # Dinamik Issue Type
        project = await asyncio.to_thread(jira.project, PROJECT_KEY)
        issue_type = next(
            (
                it.name
                for it in project.issueTypes
                if it.name.lower() in ['bug', 'xato', 'issue']
            ),
            project.issueTypes[0].name,
        )

        summary = report.split('\n')[0][:100].strip()
        new_issue = await asyncio.to_thread(
            jira.create_issue,
            fields={
                'project': PROJECT_KEY,
                'summary': summary or "New Bug",
                'description': report,
                'issuetype': {'name': issue_type},
            },
        )
        await query.edit_message_text(
            f"✅ Ochildi: [{new_issue.key}]({new_issue.permalink()})",
            parse_mode="Markdown",
        )
    except Exception as e:
        await query.message.reply_text(f"❌ Jira xatosi: {e}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(language_callback, pattern='^lang_'))
    app.add_handler(CallbackQueryHandler(jira_callback, pattern='^to_jira$'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Conflict xatosini yechish uchun eng muhim qator
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
