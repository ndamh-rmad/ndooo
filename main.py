#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import random
import threading
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from surah_audio import surahs
from commands import welcome, send_random_surah, check_bot_status

# تكوين البوت
TOKEN = "7778433338:AAH2O3DH0ZfonJ2mKeBXYSOtbjutBWvWlVQ"
CHANNEL_ID = "@dzmmm"  # استبدل بمعرف قناتك
INTERVAL = 300  # 5 دقائق بالثواني

bot = Bot(token=TOKEN)

def send_surah_to_channel():
    """إرسال سورة عشوائية إلى القناة"""
    while True:
        surah = random.choice(surahs)
        audio_url = surah["audio"]
        surah_name = surah["name"]
        reciter = "هيثم الدخين"
        
        try:
            bot.send_audio(
                chat_id=CHANNEL_ID,
                audio=audio_url,
                caption=f"سورة {surah_name}\nالقارئ: {reciter}",
                timeout=60
            )
            print(f"تم إرسال سورة {surah_name} إلى القناة")
        except Exception as e:
            print(f"حدث خطأ أثناء الإرسال: {e}")
        
        time.sleep(INTERVAL)

def start_auto_sending():
    """بدء الإرسال التلقائي في خيط منفصل"""
    thread = threading.Thread(target=send_surah_to_channel)
    thread.daemon = True
    thread.start()

def main():
    """الدالة الرئيسية لتشغيل البوت"""
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    # إضافة معالجات الأوامر
    dp.add_handler(CommandHandler("start", welcome))
    dp.add_handler(CommandHandler("surah", send_random_surah))
    dp.add_handler(CommandHandler("status", check_bot_status))

    # بدء الإرسال التلقائي
    start_auto_sending()

    # بدء البوت
    updater.start_polling()
    print("البوت يعمل الآن...")
    updater.idle()

if __name__ == "__main__":
    main()
