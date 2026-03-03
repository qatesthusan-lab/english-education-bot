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

# AI Klientini ishga tushirish
client = Groq(api_key=GROQ_API_KEY)


def get_jira_client():
    """Jira bilan ulanishni o'rnatish va URL-ni tozalash"""
    base_url = JIRA_URL.split('/jira/')[0] if '/jira/' in JIRA_URL else JIRA_URL
    return JIRA(server=base_url, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))


# Professional Senior QA Prompt
SYSTEM_PROMPT = """Siz 20 yillik tajribaga ega Senior QA Lead muhandisiz. 
Vazifangiz: Foydalanuvchi yozgan xabarni professional Jira formatiga (Summary, Steps to Reproduce, Expected/Actual Result) keltirish. 
Faqat tanlangan tilda javob bering. Javobni Markdown formatida chiroyli qiling."""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📝 Checklist & Test Case", "🐞 Bug Report"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Xush kelibsiz, Senior QA! 🤜🤛\nJira integratsiyasi va AI tayyor.\n"
        "Muammoni yozing, men uni professional formatga keltiraman.",
        reply_markup=reply_markup,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchi xabarini qabul qilish va til tanlashni so'rash"""
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
    """Tanlangan tilda AI orqali hisobot yaratish"""
    query = update.callback_query
    await query.answer()

    data = query.data
    lang_map = {'uz_lang': 'O\'zbek tili', 'ru_lang': 'Rus tili', 'en_lang': 'English'}
    if data not in lang_map:
        return

    selected_lang = lang_map[data]
    raw_text = context.user_data.get('raw_input')

    await query.edit_message_text(
        text=f"🔄 AI {selected_lang}da hisobot tayyorlamoqda, kuting..."
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
            [InlineKeyboardButton("🚀 Jira'ga yuborish", callback_data='send_to_jira')]
        ]
        await query.edit_message_text(
            text=f"📋 **Tayyorlangan Hisobot:**\n\n{report}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.error(f"AI Error: {e}")
        await query.message.reply_text(f"❌ AI Xatosi: {str(e)}")


async def jira_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ticketni dinamik Issue Type bilan Jira'ga yuborish"""
    query = update.callback_query
    await query.answer()

    report_content = context.user_data.get('last_report')
    if not report_content:
        await query.message.reply_text("Xatolik: Hisobot topilmadi.")
        return

    await query.edit_message_text(text="⏳ Jira bilan bog'lanilmoqda...")

    try:
        jira = get_jira_client()

        # 1. Dinamik Issue Type tanlash (Bug, Task, etc.)
        project = await asyncio.to_thread(jira.project, PROJECT_KEY)
        issue_types = project.issueTypes

        selected_type = None
        # Avval Bug yoki shunga o'xshashini qidiramiz
        for it in issue_types:
            if it.name.lower() in ['bug', 'ошибка', 'xato', 'issue']:
                selected_type = it.name
                break

        # Agar topilmasa, ro'yxatdagi birinchisini olamiz
        if not selected_type:
            selected_type = issue_types[0].name

        # 2. Sarlavhani tozalash
        summary_text = (
            report_content.split('\n')[0][:100]
            .replace('#', '')
            .replace('*', '')
            .strip()
        )

        # 3. Ticket yaratish
        issue_dict = {
            'project': PROJECT_KEY,
            'summary': summary_text or "Bug Report from Bot",
            'description': report_content,
            'issuetype': {'name': selected_type},
        }

        new_issue = await asyncio.to_thread(jira.create_issue, fields=issue_dict)

        await query.edit_message_text(
            text=f"✅ **JIRA TICKET OCHILDI!**\n\n🆔 ID: `{new_issue.key}`\n📂 Tur: `{selected_type}`\n🔗 [Ticketga o'tish]({new_issue.permalink()})",
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.error(f"Jira Error: {e}")
        await query.message.reply_text(
            f"❌ Jira xatosi: {str(e)}\n\nLoyiha kodi: {PROJECT_KEY}"
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Handlerlarni qo'shish
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(language_callback, pattern='_lang$'))
    app.add_handler(CallbackQueryHandler(jira_callback, pattern='^send_to_jira$'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Senior QA Bot Jira integratsiyasi bilan ishga tushdi...")
    # Eski xabarlarni o'tkazib yuborish (Conflict oldini olish uchun)
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
