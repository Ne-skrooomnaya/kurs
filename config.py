import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL', 600))
LAST_MESSAGE_ID = 177  # ваш ID

# Обязательно из .env
BYBIT_API_KEY = os.getenv('BYBIT_API_KEY')
BYBIT_SECRET_KEY = os.getenv('BYBIT_SECRET_KEY')
BYBIT_PASSPHRASE = os.getenv('BYBIT_PASSPHRASE')