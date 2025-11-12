from datetime import datetime, timezone, timedelta

def create_message(usd, eur, gold, bitcoin, updated, failed):
    utc_now = datetime.now(timezone.utc)
    moscow_time = utc_now + timedelta(hours=3)
    formatted_time = moscow_time.strftime('%Y-%m-%d %H:%M:%S')

    update_info = ", ".join(updated) if updated else "ничего"

    # Форматируем значения, если они есть
    usd_str = f"💸 USD: ₽{usd:.2f}" if usd is not None else "💸 USD: ❌"
    eur_str = f"🏆 EUR: ₽{eur:.2f}" if eur is not None else "🏆 EUR: ❌"
    gold_str = f"🌕 Золото (CFD): ${gold:,.2f}/унция" if gold is not None else "🌕 Золото (CFD): ❌"
    btc_str = f"🪩 BTC: ${bitcoin:,.0f}" if bitcoin is not None else "🪩 BTC: ❌"

    # Добавляем ⚠️ только если валюта в failed
    if 'USD' in failed and usd is not None:
        usd_str += " ⚠️"
    if 'EUR' in failed and eur is not None:
        eur_str += " ⚠️"
    if 'Золото' in failed and gold is not None:
        gold_str += " ⚠️"
    if 'BTC' in failed and bitcoin is not None:
        btc_str += " ⚠️"

    return f"""{usd_str}
{eur_str}
{gold_str}
{btc_str}

🔄 Обновлено: {update_info}
🕒 Последнее обновление: {formatted_time}
"""