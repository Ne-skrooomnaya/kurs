import asyncio
import time
import telebot
from utils import bybit_api, message_formatter, gold_api
import config

bot = telebot.TeleBot(config.TOKEN)
CHANNEL_ID = config.CHANNEL_ID

async def update_channel_info():
    while True:
        try:
            usd_rate = bybit_api.get_usd_rate()
            eur_rate = bybit_api.get_eur_rate()
            gold_price = gold_api.get_gold_price()
            bitcoin_price = bybit_api.get_bitcoin_price()

            message = message_formatter.create_message(usd_rate, eur_rate, gold_price, bitcoin_price)

            if config.LAST_MESSAGE_ID is None:
                # Отправляем первое сообщение с курсами
                new_message = bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='HTML')
                config.LAST_MESSAGE_ID = new_message.message_id
                print(f"Первое сообщение с курсами отправлено. Сохраните LAST_MESSAGE_ID = {new_message.message_id} в config.py!")

                # Закрепляем сообщение (если бот администратор)
                try:
                    bot.pin_chat_message(chat_id=CHANNEL_ID, message_id=new_message.message_id, disable_notification=True)
                    print("Сообщение закреплено!")
                except Exception as e:
                    print(f"Не удалось закрепить сообщение: {e}")
            else:
                # Редактируем только сообщение с курсами
                bot.edit_message_text(chat_id=CHANNEL_ID, message_id=config.LAST_MESSAGE_ID, text=message, parse_mode='HTML')

            print(f"Информация обновлена: {time.strftime('%Y-%m-%d %H:%M:%S')}")

        except Exception as e:
            print(f"Ошибка: {e}")

        await asyncio.sleep(config.UPDATE_INTERVAL)

async def main():
    task = asyncio.create_task(update_channel_info())
    await task

if __name__ == '__main__':
    asyncio.run(main())