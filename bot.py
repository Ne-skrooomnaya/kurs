import time
import telebot
import logging
import config
from utils import bybit_api, message_formatter, fiat_api, gold_api
from dotenv import set_key
from datetime import datetime, timezone, timedelta

# Глобальные переменные
LAST_USD = None
LAST_EUR = None
LAST_GOLD = None
LAST_BTC = None


# Логирование
class MoscowFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        utc_time = datetime.fromtimestamp(record.created, tz=timezone.utc)
        moscow_time = utc_time + timedelta(hours=3)
        if datefmt:
            return moscow_time.strftime(datefmt)
        return moscow_time.isoformat()

formatter = MoscowFormatter('%(asctime)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

bot = telebot.TeleBot(config.TOKEN)
CHANNEL_ID = config.CHANNEL_ID
_last_update = {'usd': 0, 'eur': 0, 'btc': 0, 'gold': 0}
UPDATE_INTERVAL_USD_EUR_BTC = 600
UPDATE_INTERVAL_GOLD = 900
MAIN_LOOP_INTERVAL = 300

def update_last_message_id(new_id):
    set_key('.env', 'LAST_MESSAGE_ID', str(new_id))
    config.LAST_MESSAGE_ID = new_id

def get_fresh_data():
    global LAST_USD, LAST_EUR, LAST_GOLD, LAST_BTC
    now = time.time()
    updated = []
    failed = []

    # USD
    usd = LAST_USD
    if now - _last_update['usd'] >= UPDATE_INTERVAL_USD_EUR_BTC:
        new_usd = fiat_api.get_usd_rate()
        if new_usd is not None:
            _last_update['usd'] = now
            updated.append('USD')
            LAST_USD = new_usd
            usd = new_usd
        else:
            logging.error("❌ USD не обновлено")
            failed.append('USD')

    # EUR
    eur = LAST_EUR
    if now - _last_update['eur'] >= UPDATE_INTERVAL_USD_EUR_BTC:
        new_eur = fiat_api.get_eur_rate()
        if new_eur is not None:
            _last_update['eur'] = now
            updated.append('EUR')
            LAST_EUR = new_eur
            eur = new_eur
        else:
            logging.error("❌ EUR не обновлено")
            failed.append('EUR')

    # BTC
    btc = LAST_BTC
    if now - _last_update['btc'] >= UPDATE_INTERVAL_USD_EUR_BTC:
        new_btc = bybit_api.get_bitcoin_price()
        if new_btc is not None:
            _last_update['btc'] = now
            updated.append('BTC')
            LAST_BTC = new_btc
            btc = new_btc
        else:
            logging.error("❌ BTC не обновлено")
            failed.append('BTC')

    # Gold
     # === ЗОЛОТО ===
    gold = LAST_GOLD  # ← по умолчанию — кэш
    if now - _last_update['gold'] >= UPDATE_INTERVAL_GOLD:  # каждые 15 мин
        new_gold = gold_api.get_gold_price_usd()
        if new_gold is not None:
            _last_update['gold'] = now
            updated.append('Золото')
            LAST_GOLD = new_gold
            gold = new_gold
        else:
            logging.error("❌ Золото не обновлено")
            failed.append('Золото')  # ← добавляем в failed, но gold = LAST_GOLD

    return usd, eur, gold, btc, updated, failed

def send_or_update_message():
    try:
        usd, eur, gold, btc, updated, failed = get_fresh_data()
        message = message_formatter.create_message(usd, eur, gold, btc, updated, failed)

        if config.LAST_MESSAGE_ID is None:
            new_msg = bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='HTML')
            config.LAST_MESSAGE_ID = new_msg.message_id
            update_last_message_id(new_msg.message_id)
            logging.info(f"✅ Первое сообщение. ID: {new_msg.message_id}")
        else:
            try:
                bot.edit_message_text(
                    chat_id=CHANNEL_ID,
                    message_id=config.LAST_MESSAGE_ID,
                    text=message,
                    parse_mode='HTML'
                )
                logging.info(f"✏️ Сообщение обновлено: {', '.join(updated) if updated else 'ничего'}")
            except Exception as e:
                logging.warning(f"⚠️ Не удалось отредактировать — отправляем новое: {e}")
                new_msg = bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='HTML')
                config.LAST_MESSAGE_ID = new_msg.message_id
                update_last_message_id(new_msg.message_id)

    except Exception as e:
        logging.error(f"🔥 Критическая ошибка: {e}")

if __name__ == "__main__":
    logging.info("🚀 Бот запущен")
    while True:
        send_or_update_message()
        time.sleep(MAIN_LOOP_INTERVAL)