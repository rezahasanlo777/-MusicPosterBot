import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from keep_alive import keep_alive

# ---------------- تنظیمات لاگر ----------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("__main__")

# ---------------- خواندن توکن ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("❌ BOT_TOKEN در محیط تعریف نشده!")
    raise SystemExit("توکن پیدا نشد!")

logger.info("✅ توکن با موفقیت خوانده شد")
logger.info("🚀 در حال راه‌اندازی ربات...")

# ---------------- دستورات ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام رئیس 👑 من با موفقیت روی Koyeb بالا اومدم!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

# ---------------- تابع اصلی ----------------
async def main():
    # Flask keep_alive برای health check
    keep_alive()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("🤖 Bot polling started successfully!")
    await application.run_polling()

# ---------------- اجرای مستقیم ----------------
if __name__ == "__main__":
    # چون run_polling خودش loop داره، نباید asyncio run جداگانه داشته باشیم
    import asyncio
    asyncio.run(main())
