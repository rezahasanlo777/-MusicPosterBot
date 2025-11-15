from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
import logging

# تنظیمات
TOKEN = os.environ['BOT_TOKEN']
logging.basicConfig(level=logging.INFO)

async def start(update, context):
    await update.message.reply_text(
        '🎵 **خوش اومدی به ربات موزیک فایندر!**\n\n'
        'اسم خواننده و آهنگ رو بفرست تا برات پیدا کنم!\n'
        'مثلاً: "علی سورنا آرزو"'
    )

async def handle_message(update, context):
    user_text = update.message.text
    
    # پیام زیبا برای کاربر
    message = f"""
🔥 DROP ALERT 🔥

🎧 درخواست: {user_text}
✅ به زودی آهنگ برای شما آماده می‌شود...

👑 Drop by: @musicyeooo
#PersianRap #Trap #NewDrop
    """
    
    await update.message.reply_text(message)
    
    # اینجا می‌تونی کد پیدا کردن آهنگ رو اضافه کنی
    print(f"کارگر درخواست آهنگ: {user_text}")

def main():
    app = Application.builder().token(TOKEN).build()
    
    # هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 ربات موزیک فایندر فعال شد...")
    app.run_polling()

if __name__ == '__main__':
    main()
