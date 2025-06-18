
import os
from telegram import Update
from telegram.ext import ContextTypes
from random import choice
from surah_audio import surahs

CHANNEL_ID = os.getenv('CHANNEL_ID', '@dzmmm')

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ترحيب بالمسخدم عند استخدام الأمر /start"""
    welcome_message = """
    السلام عليكم ورحمة الله وبركاته
    مرحباً بكم في بوت القرآن الكريم

    الأوامر المتاحة:
    /start - رسالة الترحيب
    /surah - إرسال سورة عشوائية
    /status - التحقق من حالة البوت
    """
    await update.message.reply_text(welcome_message)

async def send_random_surah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """إرسال سورة عشوائية إلى القناة عند الطلب"""
    surah = choice(surahs)
    audio_url = surah["audio"]
    surah_name = surah["name"]
    reciter = "مشاري راشد العفاسي"

    await context.bot.send_audio(
        chat_id=CHANNEL_ID,
        audio=audio_url,
        caption=f"سورة {surah_name}\nالقارئ: {reciter}",
        read_timeout=60,
        write_timeout=60
    )

async def check_bot_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الرد على حالة البوت"""
    status_message = "الحمد لله، البوت يعمل بشكل طبيعي 🚀"
    await update.message.reply_text(status_message)
