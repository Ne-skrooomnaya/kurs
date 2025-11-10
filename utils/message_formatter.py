import time

def create_message(usd_rate, eur_rate, gold_price, bitcoin_price):
    """Формирует сообщение с курсами."""
    if usd_rate is None or eur_rate is None or gold_price is None or bitcoin_price is None:
        return "⚠️ Не удалось получить актуальные данные."

    message = f"""💸 ₽{usd_rate:.2f}
🏆 ₽{eur_rate:.2f}
🌕 {gold_price:.2f}
🪩 ${bitcoin_price:,.0f}

Обновлено: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
    return message