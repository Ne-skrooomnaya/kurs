import requests

url = "https://api.bybit.com/v5/market/tickers"
params = {"category": "spot", "symbol": "BTCUSDT"}

response = requests.get(url, params=params)
print(response.status_code)
print(response.json())