from datetime import datetime, timezone, timedelta

def create_message(usd, eur, gold, btc, update_info):
    utc_now = datetime.now(timezone.utc)
    moscow_time = utc_now + timedelta(hours=3)
    time_str = moscow_time.strftime('%Y-%m-%d %H:%M:%S')

    lines = [
        f"💸 USD: ₽{usd:.2f}" if usd else "💸 USD: ❌",
        f"🏆 EUR: ₽{eur:.2f}" if eur else "🏆 EUR: ❌",
        f"🌕 Золото (CFD): ${gold:,.2f}/унция" if gold else "🌕 Золото (CFD): ❌",
        f"🪩 BTC: ${btc:,.0f}" if btc else "🪩 BTC: ❌",
        "",
        f"🔄 Обновлено: {update_info}",
        f"🕒 {time_str}"
    ]
    return "\n".join(lines)