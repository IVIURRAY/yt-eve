from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
from pycoingecko import CoinGeckoAPI
from eve.config import COIN_MARKET_CAP_API_KEY


class Crypto:
    def __init__(self, api_key=None):
        self.coin_market_cap = CoinMarketCap(api_key=api_key)
        self.gecko = Gecko()

    def price(self, coin, currency):
        try:
            return self.coin_market_cap.price(coin, currency)
        except CoinMarketCapAPIError:
            return self.gecko.price(coin, currency)


class CoinMarketCap:
    def __init__(self, api_key=None):
        self.api = CoinMarketCapAPI(api_key or COIN_MARKET_CAP_API_KEY)

    @staticmethod
    def filter_essential_data(data, coin, currency):
        return {
            "source": "Coin Market Cap",
            "symbol": data[coin]["symbol"],
            "name": data[coin]["name"],
            "total_supply": data[coin]["total_supply"],
            "value": f"{data[coin]['quote'][currency]['price']}",
            "currency": currency,
            "percent_change_24h": data[coin]["quote"][currency]["percent_change_24h"],
            "market_cap": data[coin]["quote"][currency]["market_cap"],
        }

    def price(self, coin, currency):
        result = self.api.cryptocurrency_quotes_latest(symbol=coin, convert=currency)
        return self.filter_essential_data(result.data, coin=coin, currency=currency)


class Gecko:
    def __init__(self):
        self.api = CoinGeckoAPI()

    @staticmethod
    def filter_essential_data(data, coin, currency):
        currency = currency.lower()
        return {
            "source": "Gecko",
            "name": coin,
            "currency": currency,
            "value": float(data[currency]),
            "percent_change_24h": data[f"{currency}_24h_change"],
            "market_cap": data[f"{currency}_market_cap"],
        }

    def price(self, coin, currency):
        result = self.api.get_price(
            ids=coin, vs_currencies=currency, include_market_cap="true", include_24hr_change="true"
        )
        return self.filter_essential_data(result[coin.lower()], coin=coin, currency=currency)
