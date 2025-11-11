import time
import telebot
import logging
import config
from utils import bybit_api, message_formatter, fiat_api, gold_api
from dotenv import set_key
from datetime import datetime, timezone, timedelta

# Настройка логирования с московским временем
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
LAST_SENT_MESSAGE = None

_last_update = {'usd': 0, 'eur': 0, 'btc': 0, 'gold': 0}
UPDATE_INTERVAL_USD_EUR_BTC = 600  # 10 минут
UPDATE_INTERVAL_GOLD = 900         # 15 минут
MAIN_LOOP_INTERVAL = 300           # проверка каждые 5 минут

def update_last_message_id(new_id):
    set_key('.env', 'LAST_MESSAGE_ID', str(new_id))
    config.LAST_MESSAGE_ID = new_id

def get_fresh_data():
    now = time.time()
    updated = []

    usd_rub = eur_rub = gold_usd = btc_usd = None

    if now - _last_update['usd'] >= UPDATE_INTERVAL_USD_EUR_BTC:
        usd_rub = fiat_api.get_usd_rate()
        if usd_rub is not None:
            _last_update['usd'] = now
            updated.append('USD')
        else:
            logging.error("❌ USD не обновлено даже через ЦБ РФ")
    else:
        usd_rub = fiat_api.get_usd_rate()

    if now - _last_update['eur'] >= UPDATE_INTERVAL_USD_EUR_BTC:
        eur_rub = fiat_api.get_eur_rate()
        if eur_rub is not None:
            _last_update['eur'] = now
            updated.append('EUR')
        else:
            logging.error("❌ EUR не обновлено даже через ЦБ РФ")
    else:
        eur_rub = fiat_api.get_eur_rate()

    if now - _last_update['btc'] >= UPDATE_INTERVAL_USD_EUR_BTC:
        btc_usd = bybit_api.get_bitcoin_price()
        if btc_usd is not None:
            _last_update['btc'] = now
            updated.append('BTC')
        else:
            logging.error("❌ BTC не обновлено")
    else:
        btc_usd = bybit_api.get_bitcoin_price()

    if now - _last_update['gold'] >= UPDATE_INTERVAL_GOLD:
        gold_usd = gold_api.get_gold_price_usd()
        if gold_usd is not None:
            _last_update['gold'] = now
            updated.append('Золото')
        else:
            logging.error("❌ Золото не обновлено")
    else:
        gold_usd = gold_api.get_gold_price_usd()

    update_info = ", ".join(updated) if updated else "ничего"
    return usd_rub, eur_rub, gold_usd, btc_usd, update_info

def send_or_update_message():
    global LAST_SENT_MESSAGE

    try:
        usd_rub, eur_rub, gold_usd, btc_usd, update_info = get_fresh_data()
        message = message_formatter.create_message(usd_rub, eur_rub, gold_usd, btc_usd, update_info)

        if config.LAST_MESSAGE_ID is None:
            new_message = bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='HTML')
            config.LAST_MESSAGE_ID = new_message.message_id
            update_last_message_id(new_message.message_id)
            logging.info(f"Первое сообщение отправлено. ID: {new_message.message_id}")
        else:
            try:
                bot.edit_message_text(chat_id=CHANNEL_ID, message_id=config.LAST_MESSAGE_ID, text=message, parse_mode='HTML')
                logging.info(f"Сообщение обновлено: {update_info}")
            except Exception as e:
                logging.error(f"Не удалось отредактировать сообщение: {e}")
                new_message = bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='HTML')
                config.LAST_MESSAGE_ID = new_message.message_id
                update_last_message_id(new_message.message_id)
                logging.info(f"Новое сообщение отправлено. ID: {new_message.message_id}")

    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    logging.info("🚀 Бот запущен. Обновление каждые 5 минут (курсы — каждые 10/15 мин).")
    while True:
        send_or_update_message()
        time.sleep(MAIN_LOOP_INTERVAL)