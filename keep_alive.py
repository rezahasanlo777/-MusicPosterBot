import zipfile
from pathlib import Path

# Create the directory structure in /mnt/data
base_dir = Path('/mnt/data/MusicPosterBot')
base_dir.mkdir(parents=True, exist_ok=True)

# --- File: keep_alive.py ---
keep_alive_code = '''from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I'm alive - MusicPosterBot by Reza Hasanloo"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
'''
(base_dir / 'keep_alive.py').write_text(keep_alive_code)

# --- File: Procfile ---
procfile_code = 'web: python keep_alive.py && python Bot.py\n'
(base_dir / 'Procfile').write_text(procfile_code)

# --- File: requirements.txt ---
requirements_code = 'pyTelegramBotAPI\nflask\nrequests\n'
(base_dir / 'requirements.txt').write_text(requirements_code)

# --- File: Bot.py (template) ---
bot_code = '''from keep_alive import keep_alive
import telebot
import os

# Environment variables (to be set in Koyeb)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')

bot = telebot.TeleBot(BOT_TOKEN)

keep_alive()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'سلام رئیس 👑! MusicPosterBot فعاله!')

# Example function to post a message to channel
@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(CHANNEL_ID, f"📨 {message.text}")

bot.infinity_polling()
'''
(base_dir / 'Bot.py').write_text(bot_code)

# Create a ZIP file
zip_path = Path('/mnt/data/MusicPosterBot_Koyeb.zip')
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file in base_dir.iterdir():
        zipf.write(file, arcname=file.name)

zip_path
