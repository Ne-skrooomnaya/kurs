# init_bot.py

import telebot
import config
from dotenv import set_key
import time

bot = telebot.TeleBot(config.TOKEN)
CHANNEL_ID = config.CHANNEL_ID

print(f"🚀 Инициализация бота. Канал: {CHANNEL_ID}")

# Отправляем тестовое сообщение
message = "🔄 Инициализация... Ожидайте обновления."
sent_msg = bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='HTML')
msg_id = sent_msg.message_id

print(f"✅ Сообщение отправлено. ID: {msg_id}")

# Закрепляем
try:
    bot.pin_chat_message(chat_id=CHANNEL_ID, message_id=msg_id, disable_notification=True)
    print("📌 Сообщение закреплено!")
except Exception as e:
    print(f"❌ Не удалось закрепить: {e}")

# Обновляем .env
set_key('.env', 'LAST_MESSAGE_ID', str(msg_id))
config.LAST_MESSAGE_ID = msg_id

print(f"💾 LAST_MESSAGE_ID сохранён в .env: {msg_id}")
print("🎉 Готово! Теперь запускайте `python bot.py`")