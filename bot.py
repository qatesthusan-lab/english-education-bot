import os
import logging
import asyncio
import google.generativeai as genai
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
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "MFT")

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# AI Sozlamalari
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')
groq_client = Groq(api_key=GROQ_API_KEY)

# Senior QA Prompt
QA_PROMPT = """Siz 20 yillik tajribaga ega Senior QA Lead va Mentorsiz. 
1. QA savollariga professional javob bering.
2. Intervyuga tayyorlang.
3. Muammolarni professional Jira formatiga (Summary, Steps, Expected, Actual) keltiring.
Foydalanuvchi qaysi tilda yozsa, o'sha tilda javob bering."""


def get_jira_client():
    base_url = JIRA_URL.split('/jira/')[0] if '/jira/' in JIRA_URL else JIRA_URL
    return JIRA(server=base_url, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))


async def get_ai_response(prompt):
    """Fallback tizimi: Gemini -> Groq"""
    try:
        # 1-urinish: Gemini
        response = await asyncio.to_thread(gemini_model.generate_content, prompt)
        return response.text
    except Exception as e:
        logger.warning(f"Gemini xatosi, Groq-ga o'tilmoqda: {e}")
        # 2-urinish: Groq (Llama 3)
        response = await asyncio.to_thread(
            groq_client.chat.completions.create,
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🐞 Bug Report", "📝 Test Case / Checklist"],
        ["👨‍🏫 QA Mentor", "💬 Erkin QA Suhbat"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Salom Senior QA Assistant ishga tushdi! Nima qilamiz?",
        reply_markup=reply_markup,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = update.effective_user.id

    # Status feedback
    status_msg = await update.message.reply_text("🤔 O'ylayapman...")

    if any(k in user_text for k in ["Bug Report", "Test Case", "Checklist"]):
        context.user_data['mode'] = 'reporting'
        await status_msg.edit_text(
            "📝 Tafsilotlarni yozing, men Jira formatiga keltiraman..."
        )
        return

    if context.user_data.get('mode') == 'reporting':
        context.user_data[f'raw_text_{user_id}'] = user_text
        context.user_data['mode'] = None
        keyboard = [
            [
                InlineKeyboardButton("🇺🇿 UZ", callback_data='lang_uz'),
                InlineKeyboardButton("🇷🇺 RU", callback_data='lang_ru'),
                InlineKeyboardButton("🇺🇸 EN", callback_data='lang_en'),
            ]
        ]
        await status_msg.edit_text(
            "Tilni tanlang:", reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    try:
        await update.message.reply_chat_action("typing")
        prompt = f"{QA_PROMPT}\nFoydalanuvchi: {user_text}"
        result = await get_ai_response(prompt)
        await status_msg.delete()
        await update.message.reply_text(result)
    except Exception as e:
        await status_msg.edit_text(f"❌ Xatolik: {str(e)}")


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    raw_input = context.user_data.get(f'raw_text_{user_id}')
    lang = query.data.split('_')[1]

    await query.edit_message_text("⏳ AI professional hisobot tayyorlamoqda...")

    try:
        prompt = f"{QA_PROMPT}\nUshbu muammoni professional Jira formatida {lang} tilida yoz: {raw_input}"
        report = await get_ai_response(prompt)
        context.user_data[f'final_report_{user_id}'] = report
        keyboard = [
            [InlineKeyboardButton("🚀 Jira'ga yuborish", callback_data='send_to_jira')]
        ]
        await query.edit_message_text(
            f"📋 **QA Report:**\n\n{report}",
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
        selected_type = next(
            (t for t in ["Bug", "Task", "Issue"] if t in types), types[0]
        )
        summary = report.split('\n')[0][:100].replace('*', '').strip()

        new_issue = await asyncio.to_thread(
            jira.create_issue,
            fields={
                'project': PROJECT_KEY,
                'summary': summary,
                'description': report,
                'issuetype': {'name': selected_type},
            },
        )
        url = f"{JIRA_URL.rstrip('/')}/browse/{new_issue.key}"
        await query.edit_message_text(
            f"✅ Ochildi: {new_issue.key}\n🔗 [Ko'rish]({url})", parse_mode="Markdown"
        )
    except Exception as e:
        await query.message.reply_text(f"❌ Jira xatosi: {str(e)}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(language_callback, pattern='^lang_'))
    app.add_handler(CallbackQueryHandler(jira_callback, pattern='^send_to_jira$'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
