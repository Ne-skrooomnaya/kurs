# utils/fiat_api.py

import requests
import config

def get_usd_rate():
    """Получает актуальный курс USD/RUB через CurrencyAPI.com."""
    if not config.CURRENCY_API_KEY:
        print("❌ CURRENCY_API_KEY не задан в .env")
        return None

    try:
        url = "https://api.currencyapi.com/v3/latest"
        params = {
            "apikey": config.CURRENCY_API_KEY,
            "base_currency": "USD",
            "currencies": "RUB"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data["data"]["RUB"]["value"])
    except requests.exceptions.Timeout:
        print("⚠️ CurrencyAPI: таймаут при запросе USD/RUB")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"⚠️ CurrencyAPI: HTTP ошибка {e.response.status_code} при запросе USD/RUB")
        return None
    except KeyError:
        print(f"❌ CurrencyAPI: неожиданный формат ответа для USD/RUB: {response.text}")
        return None
    except Exception as e:
        print(f"⚠️ Неизвестная ошибка CurrencyAPI (USD): {e}")
        return None

def get_eur_rate():
    """Получает актуальный курс EUR/RUB через CurrencyAPI.com."""
    if not config.CURRENCY_API_KEY:
        print("❌ CURRENCY_API_KEY не задан в .env")
        return None

    try:
        url = "https://api.currencyapi.com/v3/latest"
        params = {
            "apikey": config.CURRENCY_API_KEY,
            "base_currency": "EUR",
            "currencies": "RUB"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data["data"]["RUB"]["value"])
    except requests.exceptions.Timeout:
        print("⚠️ CurrencyAPI: таймаут при запросе EUR/RUB")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"⚠️ CurrencyAPI: HTTP ошибка {e.response.status_code} при запросе EUR/RUB")
        return None
    except KeyError:
        print(f"❌ CurrencyAPI: неожиданный формат ответа для EUR/RUB: {response.text}")
        return None
    except Exception as e:
        print(f"⚠️ Неизвестная ошибка CurrencyAPI (EUR): {e}")
        return None