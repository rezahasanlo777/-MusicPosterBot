import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from keep_alive import keep_alive  # اگه از keep_alive.py استفاده می‌کنی

# ---------------- تنظیمات لاگر ----------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("__main__")

# ---------------- خواندن توکن از Environment ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("❌ BOT_TOKEN در محیط تعریف نشده!")
    raise SystemExit("توکن پیدا نشد!")

logger.info("✅ توکن با موفقیت خوانده شد")
logger.info("🚀 در حال راه‌اندازی ربات...")

# ---------------- دستورات ربات ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام رئیس 👑 من با موفقیت روی Koyeb بالا اومدم!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

# ---------------- تابع اصلی ----------------
async def main():
    # فعال کردن Flask در پس‌زمینه برای health check
    keep_alive()

    application = Application.builder().token(BOT_TOKEN).build()

    # هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("🤖 Bot polling started successfully!")
    await application.run_polling(close_loop=False)

# ---------------- اجرای مستقیم ----------------
if __name__ == "__main__":
    asyncio.run(main())
