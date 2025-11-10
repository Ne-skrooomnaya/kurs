# utils/message_formatter.py

import time
from datetime import datetime, timezone, timedelta

def create_message(usd_rub, eur_rub, gold_usd, bitcoin_usd, update_info):
    if usd_rub is None or eur_rub is None or gold_usd is None or bitcoin_usd is None:
        return "⚠️ Не удалось получить актуальные данные."

    # Преобразуем UTC в Москву (UTC+3)
    utc_now = datetime.now(timezone.utc)
    moscow_time = utc_now + timedelta(hours=3)
    formatted_time = moscow_time.strftime('%Y-%m-%d %H:%M:%S')

    message = f"""💸 USD: ₽{usd_rub:.2f}
🏆 EUR: ₽{eur_rub:.2f}
🌕 Золото (CFD): ${gold_usd:,.2f}/унция
🪩 BTC: ${bitcoin_usd:,.0f}

🔄 Обновлено: {update_info}
🕒 Последнее обновление: {formatted_time}
"""
    return message