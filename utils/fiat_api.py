import requests
from bs4 import BeautifulSoup

FRANKFURTER_URL = "https://api.frankfurter.dev/v1/latest"  # ← исправлено: https://

def _get_usd_to_eur_from_frankfurter():
    try:
        response = requests.get(FRANKFURTER_URL, params={"symbols": "USD"}, timeout=15)
        response.raise_for_status()
        data = response.json()
        usd_rate = data["rates"].get("USD")
        if usd_rate:
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
    try:
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js", timeout=10)  # ← https://
        response.raise_for_status()
        data = response.json()
        eur_rub = data["Valute"]["EUR"]["Value"]
        print(f"✅ EUR/RUB из ЦБ РФ: {eur_rub:.2f}")
        return eur_rub
    except Exception as e:
        print(f"❌ Ошибка ЦБ РФ (EUR/RUB): {e}")
        return None

def _get_usd_to_rub_from_cbr():
    try:
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js", timeout=10)  # ← https://
        response.raise_for_status()
        data = response.json()
        usd_rub = data["Valute"]["USD"]["Value"]
        print(f"✅ USD/RUB напрямую из ЦБ РФ: {usd_rub:.2f}")
        return usd_rub
    except Exception as e:
        print(f"❌ Ошибка ЦБ РФ (USD/RUB): {e}")
        return None

def _get_gold_price_rub_per_gram_from_cbr():
    try:
        response = requests.get("https://cbr.ru/hd_base/metall/metall_base_new/", timeout=15)  # ← https://
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', class_='data')
        if not table:
            print("❌ ЦБ РФ: не найдена таблица с ценами на металлы")
            return None

        rows = table.find_all('tr')
        if len(rows) < 2:
            print("❌ ЦБ РФ: нет данных в таблице")
            return None

        first_data_row = rows[1]
        cells = first_data_row.find_all('td')
        if len(cells) < 2:
            print("❌ ЦБ РФ: недостаточно данных в строке")
            return None

        gold_price_str = cells[1].text.strip().replace(' ', '').replace(',', '.')
        gold_price = float(gold_price_str)
        print(f"✅ Золото из ЦБ РФ (HTML): {gold_price:.2f} ₽/грамм")
        return gold_price

    except Exception as e:
        print(f"❌ Ошибка парсинга ЦБ РФ (золото): {e}")
        return None

def get_usd_rate():
    usd_to_eur = _get_usd_to_eur_from_frankfurter()
    if usd_to_eur is None:
        print("⚠️ Не удалось получить USD/EUR → используем USD/RUB напрямую из ЦБ РФ")
        return _get_usd_to_rub_from_cbr()

    eur_to_rub = _get_eur_to_rub_from_cbr()
    if eur_to_rub is None:
        print("⚠️ Не удалось получить EUR/RUB → используем USD/RUB напрямую из ЦБ РФ")
        return _get_usd_to_rub_from_cbr()

    usd_to_rub = usd_to_eur * eur_to_rub
    print(f"✅ USD/RUB = USD/EUR × EUR/RUB = {usd_to_eur:.4f} × {eur_to_rub:.2f} = {usd_to_rub:.2f}")
    return usd_to_rub

def get_eur_rate():
    eur_rub = _get_eur_to_rub_from_cbr()
    if eur_rub is not None:
        return eur_rub
    else:
        print("⚠️ Не удалось получить EUR/RUB даже из ЦБ РФ")
        return None