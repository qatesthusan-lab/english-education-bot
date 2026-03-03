import os
import logging
import asyncio
import google.generativeai as genai
from groq import Groq  # Groq backup sifatida qoladi
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
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Railway-da buni ham qoldiring
JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "MFT")

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# AI Klientlarini sozlash
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')
groq_client = Groq(api_key=GROQ_API_KEY)


async def get_ai_response(prompt):
    """Avval Gemini-dan so'raydi, xato bo'lsa Groq-ga o'tadi"""
    try:
        # 1-urunish: Gemini
        response = await asyncio.to_thread(gemini_model.generate_content, prompt)
        return response.text
    except Exception as e:
        logger.warning(f"Gemini fail, switching to Groq: {e}")
        # 2-urunish: Groq (Llama 3)
        response = await asyncio.to_thread(
            groq_client.chat.completions.create,
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = update.effective_user.id

    # Report rejimi
    if any(k in user_text for k in ["Bug Report", "Test Case", "Checklist"]):
        await update.message.reply_text("Muammo tafsilotlarini yozing...")
        context.user_data['mode'] = 'reporting'
        return

    # Chat rejimi
    await update.message.reply_chat_action("typing")
    try:
        prompt = f"Siz Senior QA mentorsiz. Quyidagi xabarga professional javob bering: {user_text}"
        result = await get_ai_response(prompt)
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik yuz berdi: {str(e)}")


# Qolgan funksiyalar (language_callback, jira_callback) tepadagi kabi qoladi...
# Faqat AI chaqirilgan joyda 'await get_ai_response(prompt)' ishlatiladi.
