# test_message.py
import telebot
import config

bot = telebot.TeleBot(config.TOKEN)

try:
    msg = bot.get_message(chat_id=config.CHANNEL_ID, message_id=192)
    print(f"✅ Сообщение 192 найдено: {msg.text[:50]}...")
except Exception as e:
    print(f"❌ Сообщение 192 НЕ найдено: {e}")