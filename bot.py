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

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')
groq_client = Groq(api_key=GROQ_API_KEY)

# --- PROFESSIONAL MINIMALIST PROMPT ---
QA_STRICT_PROMPT = """Siz Senior QA muhandisisiz. Vazifangiz: foydalanuvchi ma'lumotini qat'iy texnik ko'rinishga keltirish.
QOIDALAR:
1. FAQAT {lang} tilida yozing.
2. Kirish va xulosa gaplarni (salom, xursandman va h.k.) mutlaqo ISHLATMANG.
3. Strukturani qat'iy saqlang:
   *Summary*: (Aniq va qisqa texnik sarlavha)
   *Env*: (OS, Version)
   *Steps*: (Faqat harakatlar, raqamlangan)
   *Expected*: (Nima bo'lishi kerak?)
   *Actual*: (Nima bo'lyapti?)
   *Severity*: (Sizning tahlilingiz bo'yicha darajasi)
4. Londa va professional bo'ling. Ortiqcha so'zlarni o'chirib tashlang."""


def get_jira_client():
    base_url = JIRA_URL.split('/jira/')[0] if '/jira/' in JIRA_URL else JIRA_URL
    return JIRA(server=base_url, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))


async def get_ai_response(prompt):
    try:
        response = await asyncio.to_thread(gemini_model.generate_content, prompt)
        return response.text
    except Exception:
        response = await asyncio.to_thread(
            groq_client.chat.completions.create,
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🐞 Bug Report", "📝 Test Case"], ["👨‍🏫 QA Mentor", "💬 Chat"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Tayyorman. Ma'lumotni yuboring.", reply_markup=reply_markup
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = update.effective_user.id

    # Jira'ga yuborish intenti
    if any(
        w in user_text.lower() for w in ["joyla", "yubor", "jira", "post"]
    ) and context.user_data.get(f'final_report_{user_id}'):
        keyboard = [
            [InlineKeyboardButton("🚀 Tasdiqlash", callback_data='send_to_jira')]
        ]
        await update.message.reply_text(
            "Jira'ga yuborilsinmi?", reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # Report yaratish boshlanishi
    if any(k in user_text for k in ["Bug Report", "Test Case"]):
        context.user_data['mode'] = 'reporting'
        await update.message.reply_text("Tafsilotlarni kiriting:")
        return

    if context.user_data.get('mode') == 'reporting':
        context.user_data[f'raw_text_{user_id}'] = user_text
        context.user_data['mode'] = None
        keyboard = [
            [
                InlineKeyboardButton("🇺🇿 UZ", callback_data='lang_uzbek'),
                InlineKeyboardButton("🇷🇺 RU", callback_data='lang_russian'),
                InlineKeyboardButton("🇺🇸 EN", callback_data='lang_english'),
            ]
        ]
        await update.message.reply_text(
            "Tilni tanlang:", reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # Chat/Mentorlik
    try:
        prompt = f"Senior QA Mentor sifatida qisqa va londa javob bering (FAQAT QA mavzusida): {user_text}"
        result = await get_ai_response(prompt)
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"Xato: {e}")


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    raw_input = context.user_data.get(f'raw_text_{user_id}')
    lang = query.data.split('_')[1]

    await query.edit_message_text("⏳ Processing...")

    try:
        full_prompt = f"{QA_STRICT_PROMPT.format(lang=lang)}\n\nINPUT: {raw_input}"
        report = await get_ai_response(full_prompt)
        context.user_data[f'final_report_{user_id}'] = report
        keyboard = [
            [InlineKeyboardButton("🚀 Jira'ga yuborish", callback_data='send_to_jira')]
        ]
        await query.edit_message_text(
            f"📋 **Report:**\n\n{report}", reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        await query.message.reply_text(f"Xato: {e}")


async def jira_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    report = context.user_data.get(f'final_report_{user_id}')

    await query.edit_message_text("⏳ Sending...")
    try:
        jira = get_jira_client()
        project = await asyncio.to_thread(jira.project, PROJECT_KEY)
        types = [it.name for it in project.issueTypes]
        selected_type = next(
            (t for t in ["Bug", "Task", "Issue"] if t in types), types[0]
        )

        # Summaryni aniq ajratib olish
        summary = "QA Report"
        for line in report.split('\n'):
            if 'Summary' in line:
                summary = line.split(':')[-1].strip()[:100]
                break

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
            f"✅ Ticket: {new_issue.key}\n🔗 [Link]({url})", parse_mode="Markdown"
        )
    except Exception as e:
        await query.message.reply_text(f"Jira Error: {e}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(language_callback, pattern='^lang_'))
    app.add_handler(CallbackQueryHandler(jira_callback, pattern='^send_to_jira$'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
