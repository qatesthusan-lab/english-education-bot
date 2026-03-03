import os
import logging
import asyncio
from groq import Groq
from jira import JIRA
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
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
Vazifangiz: Foydalanuvchi yozgan xabarni professional Jira formatiga keltirish. 
Faqat tanlangan tilda javob bering."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📝 Checklist & Test Case", "🐞 Bug Report"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Xush kelibsiz, Senior QA! 🤜🤛\nMuammoni yozing, men uni professional formatga keltiraman.",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchi xabarini saqlash va til tanlashni so'rash"""
    user_id = update.effective_user.id
    context.user_data[f'text_{user_id}'] = update.message.text
    
    keyboard = [
        [
            InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data='lang_uz'),
            InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru'),
            InlineKeyboardButton("🇺🇸 English", callback_data='lang_en')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Hisobot qaysi tilda tayyorlansin?", reply_markup=reply_markup)

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tanlangan tilda AI orqali hisobot yaratish"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    raw_text = context.user_data.get(f'text_{user_id}')
    
    if not raw_text:
        await query.edit_message_text("❌ Matn topilmadi. Iltimos, muammoni qaytadan yozing.")
        return

    lang_code = query.data.split('_')[1]
    lang_name = {'uz': 'O\'zbek tili', 'ru': 'Rus tili', 'en': 'English'}[lang_code]

    await query.edit_message_text(text=f"⏳ AI {lang_name}da hisobot tayyorlamoqda...")

    try:
        # Modelni barqarorroq va tezroq versiyaga (llama-3.1-8b) o'zgartirdik
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": f"{SYSTEM_PROMPT} Javobni faqat {lang_name}da yozing."},
                {"role": "user", "content": raw_text}
            ],
            temperature=0.3
        )
        report = response.choices[0].message.content
        context.user_data[f'report_{user_id}'] = report

        keyboard = [[InlineKeyboardButton("🚀 Jira'ga yuborish", callback_data='to_jira')]]
        await query.edit_message_text(
            text=f"📋 **Tayyorlangan Hisobot:**\n\n{report}", 
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"AI Error: {e}")
        # Xatolikning aniq sababini botda ko'rsatamiz (Debug uchun)
        await query.message.reply_text(f"❌ AI Xatosi tafsiloti: {str(e)}")

async def jira_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ticketni Jira'ga yuborish"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    report = context.user_data.get(f'report_{user_id}')
    
    if not report:
        await query.message.reply_text("❌ Hisobot topilmadi.")
        return

    await query.edit_message_text("⏳ Jira bilan bog'lanilmoqda...")

    try:
        jira = get_jira_client()
        project = await asyncio.to_thread(jira.project, PROJECT_KEY)
        issue_types = project.issueTypes
        
        selected_type = next((it.name for it in issue_types if it.name.lower() in ['bug', 'xato', 'ошибка', 'issue']), issue_types[0].name)
        summary_text = report.split('\n')[0][:100].replace('#', '').strip()

        issue_dict = {
            'project': PROJECT_KEY,
            'summary': summary_text or "Bug Report from Bot",
            'description': report,
            'issuetype': {'name': selected_type},
        }
        
        new_issue = await asyncio.to_thread(jira.create_issue, fields=issue_dict)
        await query.edit_message_text(
            text=f"✅ **JIRA TICKET OCHILDI!**\n🆔 ID: `{new_issue.key}`\n📂 Tur: `{selected_type}`\n🔗 [Link]({new_issue.permalink()})",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Jira Error: {e}")
        await query.message.reply_text(f"❌ Jira xatosi: {str(e)}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(language_callback, pattern='^lang_'))
    app.add_handler(CallbackQueryHandler(jira_callback, pattern='^to_jira$'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 Senior QA Bot ishga tushdi...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()