from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
import logging

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# خواندن توکن از environment variable
TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    logger.error("❌ توکن یافت نشد! مطمئن شوید BOT_TOKEN تنظیم شده است.")
    exit(1)

logger.info("✅ توکن با موفقیت خوانده شد")

async def start(update, context):
    user = update.effective_user
    await update.message.reply_text(
        f'🎵 **سلام {user.first_name}! به ربات موزیک فایندر خوش اومدی!**\n\n'
        '🎧 اسم خواننده و آهنگ رو بفرست تا برات پیدا کنم!\n'
        'مثلاً: "علی سورنا آرزو" یا "بهرام نوروزی"'
    )
    logger.info(f"کارگر {user.first_name} از ربات استقبال کرد")

async def handle_message(update, context):
    user_text = update.message.text
    user = update.effective_user
    
    logger.info(f"📨 درخواست از {user.first_name}: {user_text}")
    
    # پیام زیبا برای کاربر
    message = f"""
🔥 DROP ALERT 🔥

🎧 درخواست: {user_text}
✅ به زودی آهنگ برای شما آماده می‌شود...

👑 Drop by: @musicyeooo
#PersianRap #Trap #NewDrop
    """
    
    await update.message.reply_text(message)
    logger.info(f"✅ پاسخ به {user.first_name} ارسال شد")

async def error_handler(update, context):
    logger.error(f"خطا در پردازش پیام: {context.error}")

def main():
    try:
        logger.info("🚀 در حال راه‌اندازی ربات...")
        
        # ساخت اپلیکیشن
        app = Application.builder().token(TOKEN).build()
        
        # اضافه کردن هندلرها
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        app.add_error_handler(error_handler)
        
        logger.info("🤖 ربات فعال شد و در حال گوش دادن...")
        print("=" * 50)
        print("🎵 ربات موزیک فایندر فعال شد!")
        print("📞 آماده دریافت درخواست...")
        print("=" * 50)
        
        # شروع ربات
        app.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        logger.error(f"❌ خطای بحرانی: {e}")
        exit(1)

if __name__ == '__main__':
    main()
