import os
import logging
import asyncio
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, filters
)
from keep_alive import keep_alive

# 🔧 تنظیمات لاگر برای مشاهده در Koyeb Logs:
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 📦 دریافت متغیرهای محیطی از Koyeb Dashboard
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

if not BOT_TOKEN:
    logger.error("❌ BOT_TOKEN تعریف نشده!")
    raise SystemExit(1)

logger.info("✅ توکن با موفقیت خوانده شد")
logger.info("🚀 در حال راه‌اندازی ربات...")

# 🧠 تعریف دستورات پایه:
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام رئیس 👑! ربات موزیک پوستر آماده‌ست 🎵")

async def post_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not CHANNEL_ID:
        await update.message.reply_text("❌ CHANNEL_ID تنظیم نشده است")
        return
    if not update.message.audio:
        await update.message.reply_text("ارسال ناموفق 🎧 فایل صوتی بفرست رئیس.")
        return

    audio_file = update.message.audio
    caption = f"🎶 {audio_file.title or 'Track'} - {audio_file.performer or ''}"
    await context.bot.send_audio(chat_id=CHANNEL_ID, audio=audio_file.file_id, caption=caption)
    await update.message.reply_text("✅ موزیک به کانال ارسال شد!")

# 🧩 ساخت شیء اصلی Application
application = Application.builder().token(BOT_TOKEN).build()

# 🧠 ثبت هندلرها
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.AUDIO, post_music))

# ♻️ Flask keep_alive برای health check Koyeb
keep_alive()

# 🌀 نسخه سازگار با asyncio – رفع خطای stop_running_marker
async def main():
    await application.initialize()
    await application.start()
    logger.info("🤖 Bot polling started successfully!")
    await application.updater.start_polling()
    await application.updater.idle()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"❌ خطای بحرانی: {e}")
        raise
