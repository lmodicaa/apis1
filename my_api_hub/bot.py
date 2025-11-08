import os
import random
import string
import telebot
import redis

# --- CONFIGURATION ---
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN_TELEGRAM_ID = os.environ.get("ADMIN_TELEGRAM_ID", "")
REDIS_URL = os.environ.get("REDIS_URL")

def start_bot():
    bot = telebot.TeleBot(BOT_TOKEN)
    r = redis.from_url(REDIS_URL)

    print("🤖 Bot is starting...")

    @bot.message_handler(commands=['start', 'getcode'])
    def send_welcome(message):
        user_id = message.chat.id
        code = ''.join(random.choices(string.digits, k=6))
        r.set(f"code:{code}", user_id, ex=300)
        bot.reply_to(message,
            f"👋 Hello!\n\nYour one-time access code for ApiHub is:\n\n➡️ `{code}` ⬅️\n\nThis code is valid for 5 minutes.",
            parse_mode="Markdown"
        )

    @bot.message_handler(commands=['stats'])
    def send_stats(message):
        if str(message.chat.id) == str(ADMIN_TELEGRAM_ID):
            bot.reply_to(message, "📊 Stats feature is under development in this new setup.")
        else:
            bot.reply_to(message, "Sorry, you are not authorized.")

    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"❌ Bot crashed: {e}. Restarting...")
        start_bot()
