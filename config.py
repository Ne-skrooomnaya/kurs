import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))  # ← int, так как это ID канала
LAST_MESSAGE_ID = int(os.getenv('LAST_MESSAGE_ID')) if os.getenv('LAST_MESSAGE_ID') else None

FMP_API_KEY = os.getenv('FMP_API_KEY')