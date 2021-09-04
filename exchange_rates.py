import requests as requests


class ExchangeRates():
    def __init__(self):
        self.request_eur_usd_rate = "http://api.exchangeratesapi.io/v1/latest?access_key=3b48219c348eac29d1864dba3494e857&symbols=USD"

    def fetch_latest_eur_usd_rate(self):
        response = requests.get(self.request_eur_usd_rate)
        return response.json()['rates']['USD']
