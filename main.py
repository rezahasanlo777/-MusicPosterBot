import os
from telegram.ext import Application, MessageHandler, filters
import logging

# تنظیمات لاگینگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# گرفتن توکن و Channel ID از متغیرهای محیطی
# (این متغیرها را در پنل Railway وارد خواهید کرد)
BOT_TOKEN = os.getenv("BOT_TOKEN")
# آیدی کانال مقصد (مثلاً: @channelusername یا -100xxxxxxxxxx)
CHANNEL_ID = os.getenv("CHANNEL_ID") 

# تابع اصلی برای بازنشر فایل صوتی
async def repost_audio(update, context):
    # این کد مطمئن می‌شود که پیام حاوی فایل صوتی است
    if update.message.audio:
        audio = update.message.audio
        caption = update.message.caption or "" # کپشن فایل را اگر وجود داشت می‌خواند

        try:
            # ارسال فایل صوتی به کانال مقصد
            await context.bot.send_audio(
                chat_id=CHANNEL_ID,
                audio=audio.file_id,
                caption=caption,
                title=audio.title,
                performer=audio.performer,
            )
            logging.info(f"Audio reposted successfully from {update.message.from_user.username} to {CHANNEL_ID}")
            
            # پاسخ به فرستنده برای تایید دریافت
            await update.message.reply_text("فایل صوتی با موفقیت دریافت و در حال بازنشر است.")
            
        except Exception as e:
            logging.error(f"Error reposting audio: {e}")
            await update.message.reply_text(f"خطا در بازنشر فایل صوتی: {e}")
            
    else:
        # اگر فایل صوتی نبود، پاسخ می‌دهد
        await update.message.reply_text("لطفاً یک فایل صوتی (Audio) ارسال کنید تا پردازش شود.")


def main():
    """شروع به کار ربات"""
    if not BOT_TOKEN:
        logging.error("BOT_TOKEN environment variable not set. Exiting.")
        return
    
    if not CHANNEL_ID:
        logging.warning("CHANNEL_ID environment variable not set. Reposting will likely fail until it is set on the host.")

    # ساخت اپلیکیشن
    application = Application.builder().token(BOT_TOKEN).build()

    # هندلر برای دریافت هر پیامی که حاوی فایل صوتی باشد
    application.add_handler(MessageHandler(filters.AUDIO, repost_audio))

    # اجرای ربات به صورت نظرسنجی (Polling)
    logging.info("Bot started and running in Polling mode...")
    application.run_polling(poll_interval=1.0, allowed_updates=list(range(13)))


if __name__ == '__main__':
    main()
