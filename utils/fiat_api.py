# utils/fiat_api.py

import requests

FRANKFURTER_URL = "https://api.frankfurter.dev/v1/latest"

def _get_usd_to_eur_from_frankfurter():
    """Получает USD/EUR через Frankfurter (база EUR -> rates.USD = сколько USD за 1 EUR)."""
    try:
        response = requests.get(
            FRANKFURTER_URL,
            params={"symbols": "USD"},
            timeout=15
        )
        response.raise_for_status()
        data = response.json()
        usd_rate = data["rates"].get("USD")
        if usd_rate:
            # USD/EUR = 1 / (EUR/USD)
            usd_to_eur = 1.0 / float(usd_rate)
            print(f"✅ USD/EUR из Frankfurter: {usd_to_eur:.4f}")
            return usd_to_eur
        else:
            print("❌ Frankfurter: USD не найден")
            return None
    except Exception as e:
        print(f"⚠️ Ошибка Frankfurter (USD/EUR): {e}")
        return None

def _get_eur_to_rub_from_cbr():
    """Получает EUR/RUB напрямую из ЦБ РФ."""
    try:
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js", timeout=10)
        response.raise_for_status()
        data = response.json()
        eur_rub = data["Valute"]["EUR"]["Value"]
        print(f"✅ EUR/RUB из ЦБ РФ: {eur_rub:.2f}")
        return eur_rub
    except Exception as e:
        print(f"❌ Ошибка ЦБ РФ (EUR/RUB): {e}")
        return None

def _get_usd_to_rub_from_cbr():
    """Резервный fallback: USD/RUB напрямую из ЦБ РФ."""
    try:
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js", timeout=10)
        response.raise_for_status()
        data = response.json()
        usd_rub = data["Valute"]["USD"]["Value"]
        print(f"✅ USD/RUB напрямую из ЦБ РФ: {usd_rub:.2f}")
        return usd_rub
    except Exception as e:
        print(f"❌ Ошибка ЦБ РФ (USD/RUB): {e}")
        return None

def get_usd_rate():
    # Шаг 1: Получить USD/EUR
    usd_to_eur = _get_usd_to_eur_from_frankfurter()
    if usd_to_eur is None:
        # Если не удалось — fallback на прямой USD/RUB из ЦБ
        print("⚠️ Не удалось получить USD/EUR → используем USD/RUB напрямую из ЦБ РФ")
        return _get_usd_to_rub_from_cbr()

    # Шаг 2: Получить EUR/RUB
    eur_to_rub = _get_eur_to_rub_from_cbr()
    if eur_to_rub is None:
        print("⚠️ Не удалось получить EUR/RUB → используем USD/RUB напрямую из ЦБ РФ")
        return _get_usd_to_rub_from_cbr()

    # Шаг 3: Вычислить USD/RUB = USD/EUR * EUR/RUB
    usd_to_rub = usd_to_eur * eur_to_rub
    print(f"✅ USD/RUB = USD/EUR × EUR/RUB = {usd_to_eur:.4f} × {eur_to_rub:.2f} = {usd_to_rub:.2f}")
    return usd_to_rub

def get_eur_rate():
    # Для EUR/RUB — просто берём из ЦБ РФ
    eur_rub = _get_eur_to_rub_from_cbr()
    if eur_rub is not None:
        return eur_rub
    else:
        print("⚠️ Не удалось получить EUR/RUB даже из ЦБ РФ")
        return None