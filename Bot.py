import os
import logging
import asyncio
from threading import Thread
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from keep_alive import keep_alive  # Flask server for Koyeb health checks

# ---------------- تنظیم لاگر ----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ---------------- هندلِرها ----------------
async def start(update, context):
    await update.message.reply_text("سلام رئیس! رباتت آنلاینه 🎵")

async def echo(update, context):
    await update.message.reply_text(update.message.text)

# ---------------- تابع اصلی ----------------
async def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("🤖 Bot polling started successfully!")
    await application.run_polling()

# ---------------- اجرای برنامه ----------------
if __name__ == "__main__":
    logger.info("✅ توکن با موفقیت خوانده شد")
    logger.info("🚀 در حال راه‌اندازی ربات...")

    # اجرای Flask برای health check در thread جداگانه
    Thread(target=keep_alive).start()

    # اجرای async main در event loop اصلی
    asyncio.run(main())
