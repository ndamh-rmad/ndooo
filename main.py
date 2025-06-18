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

# تكوين البوت
TOKEN = "7778433338:AAH2O3DH0ZfonJ2mKeBXYSOtbjutBWvWlVQ"
CHANNEL_ID = "@dzmmm"
INTERVAL = 300  # 5 دقائق بالثواني

# إعدادات التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def send_surah_to_channel():
    """إرسال سورة عشوائية إلى القناة"""
    bot = Bot(token=TOKEN)
    while True:
        try:
            surah = random.choice(surahs)
            audio_url = surah["audio"]
            surah_name = surah["name"]
            reciter = "هيثم الدخين"
            
            await bot.send_audio(
                chat_id=CHANNEL_ID,
                audio=audio_url,
                caption=f"سورة {surah_name}\nالقارئ: {reciter}",
                read_timeout=60,
                write_timeout=60
            )
            logger.info(f"تم إرسال سورة {surah_name} إلى القناة")
        except Exception as e:
            logger.error(f"حدث خطأ أثناء الإرسال: {e}")
        
        await asyncio.sleep(INTERVAL)

def main() -> None:
    """الدالة الرئيسية لتشغيل البوت"""
    application = Application.builder().token(TOKEN).build()
    
    # إضافة معالجات الأوامر
    application.add_handler(CommandHandler("start", welcome))
    application.add_handler(CommandHandler("surah", send_random_surah))
    application.add_handler(CommandHandler("status", check_bot_status))
    
    # بدء الإرسال التلقائي في الخلفية
    loop = asyncio.get_event_loop()
    loop.create_task(send_surah_to_channel())
    
    # بدء البوت
    logger.info("البوت يعمل الآن...")
    application.run_polling()

if __name__ == "__main__":
    main()
