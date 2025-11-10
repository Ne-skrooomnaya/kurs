# utils/message_formatter.py

import time

def create_message(usd_rub, eur_rub, gold_usd, bitcoin_usd, update_info):
    if usd_rub is None or eur_rub is None or gold_usd is None or bitcoin_usd is None:
        return "⚠️ Не удалось получить актуальные данные."

    message = f"""💸 USD: ₽{usd_rub:.2f}
🏆 EUR: ₽{eur_rub:.2f}
🌕 Золото (CFD): ${gold_usd:,.2f}/унция
🪩 BTC: ${bitcoin_usd:,.0f}

🔄 Обновлено: {update_info}
🕒 Последнее обновление: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
    return message