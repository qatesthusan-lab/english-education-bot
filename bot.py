import os
import logging
import asyncio
import google.generativeai as genai
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
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "MFT")

# Gemini Sozlamalari
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_jira_client():
    base_url = JIRA_URL.split('/jira/')[0] if '/jira/' in JIRA_URL else JIRA_URL
    return JIRA(server=base_url, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))


# --- SENIOR QA MENTOR PROMPT ---
QA_CORE_PROMPT = """Siz 20 yillik tajribaga ega Senior QA Lead va Mentorsiz. 
Vazifalaringiz:
1. Foydalanuvchi bilan QA mavzusida (Manual, Automation, API, Mobile, Security testing) professional suhbatlashish.
2. Intervyu savollariga javob berish va foydalanuvchini intervyuga tayyorlash.
3. Agar foydalanuvchi muammo yozsa, uni professional Jira formatida (Bug Report, Test Case yoki Checklist) tayyorlash.
4. Javobingiz qisqa, aniq va Senior darajasida bo'lsin.
5. Foydalanuvchi qaysi tilda murojaat qilsa (UZ, RU, EN), o'sha tilda javob bering."""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🐞 Bug Report", "📝 Test Case / Checklist"],
        ["👨‍🏫 QA Interview Prep", "💬 Erkin QA Suhbat"],
        ["❓ Yordam"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Xush kelibsiz, Senior QA Assistant ishga tushdi! ✨\n\n"
        "Men sizga bug reportlar yozishda, test caselar tuzishda va "
        "QA intervyulariga tayyorlanishda yordam beraman. Gemini AI kuchi bilan!",
        reply_markup=reply_markup,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = update.effective_user.id

    # Report yaratish rejimini aniqlash
    report_keywords = ["Bug Report", "Test Case", "Checklist"]
    if any(k in user_text for k in report_keywords):
        await update.message.reply_text(
            "Iltimos, muammo yoki test qilinishi kerak bo'lgan funksiya haqida yozing..."
        )
        context.user_data['mode'] = 'reporting'
        return

    # Agar reporting rejimida bo'lsa
    if context.user_data.get('mode') == 'reporting':
        context.user_data[f'raw_text_{user_id}'] = user_text
        context.user_data['mode'] = None

        keyboard = [
            [
                InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data='lang_uz'),
                InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru'),
                InlineKeyboardButton("🇺🇸 English", callback_data='lang_en'),
            ]
        ]
        await update.message.reply_text(
            "Hisobot qaysi tilda tayyorlansin?",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

    # ERKIN SUHBAT VA MENTORLIK (Gemini)
    await update.message.reply_chat_action("typing")
    try:
        full_context = f"{QA_CORE_PROMPT}\nFoydalanuvchi xabari: {user_text}"
        response = await asyncio.to_thread(model.generate_content, full_context)
        await update.message.reply_text(response.text)
    except Exception as e:
        logger.error(f"Gemini Error: {e}")
        await update.message.reply_text(
            "❌ Gemini AI bilan ulanishda xatolik yuz berdi."
        )


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    raw_input = context.user_data.get(f'raw_text_{user_id}')
    lang_code = query.data.split('_')[1]
    lang_name = {'uz': 'O\'zbek tili', 'ru': 'Rus tili', 'en': 'English'}[lang_code]

    await query.edit_message_text(
        f"⏳ Gemini {lang_name}da professional hisobot tuzmoqda..."
    )

    try:
        report_prompt = f"{QA_CORE_PROMPT}\nFoydalanuvchi matnini faqat {lang_name}da professional Jira formatiga keltir: {raw_input}"
        response = await asyncio.to_thread(model.generate_content, report_prompt)
        report_text = response.text
        context.user_data[f'final_report_{user_id}'] = report_text

        keyboard = [
            [
                InlineKeyboardButton(
                    "🚀 Jira'ga yuborish (MFT)", callback_data='send_to_jira'
                )
            ]
        ]
        await query.edit_message_text(
            f"📋 **Tayyorlangan QA Report:**\n\n{report_text}",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    except Exception as e:
        await query.message.reply_text(f"❌ Xatolik: {str(e)}")


async def jira_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    report = context.user_data.get(f'final_report_{user_id}')

    await query.edit_message_text("⏳ Jira-ga yuborilmoqda...")

    try:
        jira = get_jira_client()
        project = await asyncio.to_thread(jira.project, PROJECT_KEY)
        types = [it.name for it in project.issueTypes]
        # Eng mos turni tanlash
        selected_type = next(
            (t for t in ["Bug", "Task", "Issue", "Ошибка"] if t in types), types[0]
        )

        summary = report.split('\n')[0][:100].replace('*', '').replace('#', '').strip()
        new_issue = await asyncio.to_thread(
            jira.create_issue,
            fields={
                'project': PROJECT_KEY,
                'summary': summary or "New QA Document",
                'description': report,
                'issuetype': {'name': selected_type},
            },
        )

        issue_url = f"{JIRA_URL.rstrip('/')}/browse/{new_issue.key}"
        await query.edit_message_text(
            text=f"✅ **Jirada Ticket Ochildi!**\n🆔 ID: `{new_issue.key}`\n📂 Tur: `{selected_type}`\n🔗 [Ticketga o'tish]({issue_url})",
            parse_mode="Markdown",
        )
    except Exception as e:
        await query.message.reply_text(f"❌ Jira xatosi: {str(e)}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(language_callback, pattern='^lang_'))
    app.add_handler(CallbackQueryHandler(jira_callback, pattern='^send_to_jira$'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Gemini QA Assistant ishga tushdi...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
