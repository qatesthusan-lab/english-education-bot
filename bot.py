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

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# AI Klientlarini sozlash
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')
groq_client = Groq(api_key=GROQ_API_KEY)

# --- SENIOR QA PROMPT STANDARTI ---
QA_SYSTEM_PROMPT = """Siz 20 yillik tajribaga ega Senior QA Lead va Mentorsiz. 
Sizning vazifangiz:
1. Foydalanuvchi bilan QA mavzusida professional suhbatlashish va intervyuga tayyorlash.
2. Bug Report yaratishda FAQAT tanlangan tilda ({lang}) quyidagi strukturani qo'llash:
   - **Summary**: Qisqa sarlavha
   - **Environment**: OS, Browser, App Version
   - **Preconditions**: Dastlabki shartlar
   - **Steps to Reproduce**: Qadamlar
   - **Expected Result**: Kutilgan natija
   - **Actual Result**: Haqiqiy natija
   - **Severity**: Darajasi
3. Tanlangan tildan boshqa tilda javob bermang!"""


def get_jira_client():
    base_url = JIRA_URL.split('/jira/')[0] if '/jira/' in JIRA_URL else JIRA_URL
    return JIRA(server=base_url, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))


async def get_ai_response(prompt):
    """Gemini ishlamasa Groq-ga o'tuvchi Fallback tizimi"""
    try:
        response = await asyncio.to_thread(gemini_model.generate_content, prompt)
        return response.text
    except Exception as e:
        logger.warning(f"Gemini xatosi, Groq-ga o'tildi: {e}")
        response = await asyncio.to_thread(
            groq_client.chat.completions.create,
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🐞 Bug Report", "📝 Test Case"],
        ["👨‍🏫 QA Mentor", "💬 Erkin Suhbat"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Salom Senior QA! Men sizning professional asistentingizman.\n"
        "Bug report yozamizmi yoki QA haqida suhbatlashamizmi?",
        reply_markup=reply_markup,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = update.effective_user.id

    # Intent 1: Jira'ga yuborish
    jira_cmd = ["joyla", "yubor", "jira", "send", "post"]
    if any(w in user_text.lower() for w in jira_cmd) and context.user_data.get(
        f'final_report_{user_id}'
    ):
        keyboard = [
            [
                InlineKeyboardButton(
                    "🚀 Jira'ga yuborishni tasdiqlash", callback_data='send_to_jira'
                )
            ]
        ]
        await update.message.reply_text(
            "Oxirgi hisobotni Jira'ga joylaymi?",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

    # Intent 2: Report yaratish rejimi
    if any(k in user_text for k in ["Bug Report", "Test Case"]):
        context.user_data['mode'] = 'reporting'
        await update.message.reply_text(
            "📝 Muammo tafsilotlarini yozing (Muhit, qadamlar, kutilgan natija):"
        )
        return

    # Rejim: Ma'lumot qabul qilish
    if context.user_data.get('mode') == 'reporting':
        context.user_data[f'raw_text_{user_id}'] = user_text
        context.user_data['mode'] = None
        keyboard = [
            [
                InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data='lang_uzbek'),
                InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_russian'),
                InlineKeyboardButton("🇺🇸 English", callback_data='lang_english'),
            ]
        ]
        await update.message.reply_text(
            "Hisobot qaysi tilda tuzilsin?", reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # Intent 3: QA Mentorlik (Chat)
    status_msg = await update.message.reply_text("🤔 O'ylayapman...")
    try:
        prompt = f"Siz Senior QA mentorsiz. Quyidagi xabarga o'sha tilda professional javob bering: {user_text}"
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

    await query.edit_message_text(
        f"⏳ AI {lang} tilida professional report tuzmoqda..."
    )

    try:
        # Tilni qat'iy nazorat qilish uchun prompt
        full_prompt = f"{QA_SYSTEM_PROMPT.format(lang=lang)}\n\nFoydalanuvchi ma'lumoti: {raw_input}\n\nFAQAT {lang} tilida javob ber!"
        report = await get_ai_response(full_prompt)
        context.user_data[f'final_report_{user_id}'] = report

        keyboard = [
            [InlineKeyboardButton("🚀 Jira'ga yuborish", callback_data='send_to_jira')]
        ]
        await query.edit_message_text(
            f"📋 **Tayyor QA Report:**\n\n{report}",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    except Exception as e:
        await query.message.reply_text(f"❌ Xatolik: {str(e)}")


async def jira_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    report = context.user_data.get(f'final_report_{user_id}')

    await query.edit_message_text("⏳ Jira'ga ticket ochilmoqda...")
    try:
        jira = get_jira_client()
        project = await asyncio.to_thread(jira.project, PROJECT_KEY)
        types = [it.name for it in project.issueTypes]
        selected_type = next(
            (t for t in ["Bug", "Task", "Issue"] if t in types), types[0]
        )

        # Summaryni reportning birinchi qatoridan olish
        summary = (
            report.split('\n')[0]
            .replace('Summary:', '')
            .replace('**', '')
            .strip()[:100]
        )

        new_issue = await asyncio.to_thread(
            jira.create_issue,
            fields={
                'project': PROJECT_KEY,
                'summary': summary or "New QA Bug Report",
                'description': report,
                'issuetype': {'name': selected_type},
            },
        )
        url = f"{JIRA_URL.rstrip('/')}/browse/{new_issue.key}"
        await query.edit_message_text(
            f"✅ Muvaffaqiyatli! Ticket ID: `{new_issue.key}`\n🔗 [Jirada ko'rish]({url})",
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
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
