import os
import logging
import asyncio
from groq import Groq
from jira import JIRA
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
)

# --- KONFIGURATSIYA ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "MFT")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

client = Groq(api_key=GROQ_API_KEY)

def get_jira_client():
    base_url = JIRA_URL.split('/jira/')[0] if '/jira/' in JIRA_URL else JIRA_URL
    return JIRA(server=base_url, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📝 Checklist & Test Case", "🐞 Bug Report"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Salom Senior QA! Muammoni yozing, men uni Jira formatiga keltiraman:", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    context.user_data[f'text_{user_id}'] = update.message.text
    
    keyboard = [[
        InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data='lang_uzbek'),
        InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_russian'),
        InlineKeyboardButton("🇺🇸 English", callback_data='lang_english')
    ]]
    await update.message.reply_text("Qaysi tilda hisobot kerak?", reply_markup=InlineKeyboardMarkup(keyboard))

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    raw_text = context.user_data.get(f'text_{user_id}')
    
    if not raw_text:
        await query.edit_message_text("❌ Matn yo'qolgan. Qaytadan yozing.")
        return

    selected_lang = query.data.split('_')[1]
    await query.edit_message_text(f"⏳ AI {selected_lang.capitalize()} tilida tayyorlamoqda...")

    try:
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": f"You are a Senior QA. Write a detailed Jira report in {selected_lang}. Include Summary, Steps, Expected, and Actual results. Use plain text only."},
                {"role": "user", "content": f"Format this into a {selected_lang} report: {raw_text}"}
            ],
            temperature=0.1
        )
        report = response.choices[0].message.content
        context.user_data[f'report_{user_id}'] = report

        keyboard = [[InlineKeyboardButton("🚀 Jira'ga yuborish", callback_data='to_jira')]]
        await query.edit_message_text(f"📋 **Hisobot ({selected_lang.capitalize()}):**\n\n{report}", reply_markup=InlineKeyboardMarkup(keyboard))
    except Exception as e:
        await query.message.reply_text(f"❌ AI Xatosi: {str(e)}")

async def jira_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    report = context.user_data.get(f'report_{user_id}')
    
    await query.edit_message_text("⏳ Jira bilan bog'lanilmoqda...")

    try:
        jira = get_jira_client()
        
        # --- MUAMMONING YECHIMI SHU YERDA ---
        # Loyihadagi ruxsat berilgan barcha "Issue Type"larni olamiz
        project = await asyncio.to_thread(jira.project, PROJECT_KEY)
        available_types = [it.name for it in project.issueTypes]
        
        # Eng mos keladiganini tanlaymiz
        selected_type = None
        for t in ["Bug", "Ошибка", "Task", "Story", "Issue"]:
            if t in available_types:
                selected_type = t
                break
        
        if not selected_type:
            selected_type = available_types[0] # Agar hech biri topilmasa, birinchisini olamiz

        summary = report.split('\n')[0][:100].replace('#', '').strip()
        
        issue_dict = {
            'project': PROJECT_KEY,
            'summary': summary or "New QA Bug",
            'description': report,
            'issuetype': {'name': selected_type}
        }

        new_issue = await asyncio.to_thread(jira.create_issue, fields=issue_dict)
        clean_url = f"{JIRA_URL.rstrip('/')}/browse/{new_issue.key}"
        
        await query.edit_message_text(f"✅ **Muvaffaqiyatli!**\n🆔 ID: `{new_issue.key}`\n📂 Tur: `{selected_type}`\n🔗 [Jirada ko'rish]({clean_url})", parse_mode="Markdown")
    except Exception as e:
        await query.message.reply_text(f"❌ Jira xatosi: {str(e)}\n(Mavjud turlar: {', '.join(available_types) if 'available_types' in locals() else 'Noma'lum'})")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(language_callback, pattern='^lang_'))
    app.add_handler(CallbackQueryHandler(jira_callback, pattern='^to_jira$'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()