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
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

client = Groq(api_key=GROQ_API_KEY)


def get_jira_client():
    base_url = JIRA_URL.split('/jira/')[0] if '/jira/' in JIRA_URL else JIRA_URL
    return JIRA(server=base_url, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📝 Checklist & Test Case", "🐞 Bug Report"],
        ["👨‍🏫 Interview Mentor"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Xush kelibsiz! Bug yoki Test Case haqida yozing, men uni professional formatga keltiraman.",
        reply_markup=reply_markup,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Foydalanuvchi matnini saqlaymiz
    context.user_data['raw_input'] = update.message.text

    # Tilni tanlash tugmalari
    keyboard = [
        [
            InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data='lang_uz'),
            InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru'),
            InlineKeyboardButton("🇺🇸 English", callback_data='lang_en'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hisobot qaysi tilda bo'lsin?", reply_markup=reply_markup
    )


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang_map = {'lang_uz': 'O\'zbek tili', 'lang_ru': 'Rus tili', 'lang_en': 'English'}
    selected_lang = lang_map[query.data]
    raw_text = context.user_data.get('raw_input')

    # AI orqali tanlangan tilda hisobot tayyorlash
    response = await asyncio.to_thread(
        client.chat.completions.create,
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"Siz Senior QA-siz. Hisobotni {selected_lang}da professional Jira formatida tayyorlang.",
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
                "🚀 Jira'ga yuborish (MFT loyihasiga)", callback_data='send_to_jira'
            )
        ]
    ]
    await query.edit_message_text(
        text=f"📋 **Tayyorlangan Hisobot ({selected_lang}):**\n\n{report}",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def jira_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    report_content = context.user_data.get('last_report')

    try:
        jira = get_jira_client()
        summary = report_content.split('\n')[0][:100].replace('#', '').strip()

        issue_dict = {
            'project': PROJECT_KEY,
            'summary': summary,
            'description': report_content,
            'issuetype': {'name': 'Bug'},
        }

        new_issue = await asyncio.to_thread(jira.create_issue, fields=issue_dict)
        await query.edit_message_text(
            text=f"✅ **JIRA TICKET OCHILDI!**\n\n🆔 Key: `{new_issue.key}`\n🔗 [Ticketga o'tish]({new_issue.permalink()})",
            parse_mode="Markdown",
        )
    except Exception as e:
        await query.message.reply_text(f"❌ Jira xatosi: {str(e)}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(language_callback, pattern='^lang_'))
    app.add_handler(CallbackQueryHandler(jira_callback, pattern='send_to_jira'))
    app.run_polling()


if __name__ == "__main__":
    main()
