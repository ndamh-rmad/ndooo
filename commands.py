from telegram import ParseMode
from random import choice
from surah_audio import surahs

def welcome(update, context):
    """ترحيب بالمسخدم عند استخدام الأمر /start"""
    welcome_message = """
    السلام عليكم ورحمة الله وبركاته
    مرحباً بكم في بوت القرآن الكريم
    
    الأوامر المتاحة:
    /start - رسالة الترحيب
    /surah - إرسال سورة عشوائية
    /status - التحقق من حالة البوت
    """
    update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)

def send_random_surah(update, context):
    """إرسال سورة عشوائية عند الطلب"""
    surah = choice(surahs)
    audio_url = surah["audio"]
    surah_name = surah["name"]
    reciter = "هيثم الدخين"
    
    context.bot.send_audio(
        chat_id=update.message.chat_id,
        audio=audio_url,
        caption=f"سورة {surah_name}\nالقارئ: {reciter}",
        timeout=60
    )

def check_bot_status(update, context):
    """الرد على حالة البوت"""
    status_message = "الحمد لله، البوت يعمل بشكل طبيعي 🚀"
    update.message.reply_text(status_message)
