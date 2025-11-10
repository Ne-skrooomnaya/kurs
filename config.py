import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL', 600))
LAST_MESSAGE_ID = int(os.getenv('LAST_MESSAGE_ID')) if os.getenv('LAST_MESSAGE_ID') else None

GOLD_API_KEY = os.getenv('GOLD_API_KEY')
CURRENCY_API_KEY = os.getenv('CURRENCY_API_KEY')