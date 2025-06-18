import os
import time
import random
import logging
import asyncio
from telegram import Bot
from telegram.ext import Application, CommandHandler
from surah_audio import surahs
from commands import welcome, send_random_surah, check_bot_status

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHANNEL_ID = "@dzmmm"
INTERVAL = 300

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def send_surah_to_channel(application):
    bot = application.bot
    while True:
        try:
            surah = random.choice(surahs)
            await bot.send_audio(
                chat_id=CHANNEL_ID,
                audio=surah["audio"],
                caption=f"سورة {surah['name']}\nالقارئ: مشاري راشد",
                read_timeout=60,
                write_timeout=60
            )
            logger.info(f"✅ تم إرسال سورة {surah['name']} إلى القناة.")
        except Exception as e:
            logger.error(f"❌ خطأ أثناء الإرسال: {e}")
        await asyncio.sleep(INTERVAL)

async def start_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", welcome))
    application.add_handler(CommandHandler("surah", send_random_surah))
    application.add_handler(CommandHandler("status", check_bot_status))
    application.job_queue.run_once(lambda *_: asyncio.create_task(send_surah_to_channel(application)), 1)
    logger.info("🚀 البوت يعمل الآن...")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(start_bot())
