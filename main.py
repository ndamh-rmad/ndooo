#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import random
import asyncio
import logging
from telegram import Bot
from telegram.ext import Application, CommandHandler
from surah_audio import surahs
from commands import welcome, send_random_surah, check_bot_status

# إعدادات البيئة
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHANNEL_ID = "@dzmmm"
INTERVAL = 300  # إرسال كل 5 دقائق

# إعدادات اللوق
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# إرسال سورة عشوائية للقناة
async def send_surah_to_channel():
    bot = Bot(token=TOKEN)
    while True:
        try:
            surah = random.choice(surahs)
            audio_url = surah["audio"]
            surah_name = surah["name"]
            reciter = "مشاري راشد العفاسي"

            await bot.send_audio(
                chat_id=CHANNEL_ID,
                audio=audio_url,
                caption=f"سورة {surah_name}\nالقارئ: {reciter}",
                read_timeout=60,
                write_timeout=60
            )
            logger.info(f"✅ تم إرسال سورة {surah_name} إلى القناة.")
        except Exception as e:
            logger.error(f"❌ خطأ أثناء الإرسال: {e}")

        await asyncio.sleep(INTERVAL)

# دالة التشغيل الأساسية
async def main():
    application = Application.builder().token(TOKEN).build()

    # حذف Webhook لتفادي تضارب الجلسات
    await application.bot.delete_webhook(drop_pending_updates=True)

    # أوامر البوت
    application.add_handler(CommandHandler("start", welcome))
    application.add_handler(CommandHandler("surah", send_random_surah))
    application.add_handler(CommandHandler("status", check_bot_status))

    # مهمة الإرسال التلقائي
    asyncio.create_task(send_surah_to_channel())

    logger.info("🚀 البوت يعمل الآن...")
    await application.run_polling()

# لتشغيل البوت في بيئات async مثل Render
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())

