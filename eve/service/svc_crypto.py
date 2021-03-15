from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
from eve.config import COIN_MARKET_CAP_API_KEY


class Crypto:

    def __init__(self, api_key=None):
        self.manager = CoinMarketCapAPI(api_key or COIN_MARKET_CAP_API_KEY)

    @staticmethod
    def filter_essential_data(data, coin, currency):
        return {
            'symbol': data[coin]["symbol"],
            'name': data[coin]["name"],
            'total_supply': data[coin]["total_supply"],
            'price': f"{data[coin]['quote'][currency]['price']} {currency}",
            'percent_change_24h': data[coin]["quote"][currency]["percent_change_24h"],
            'market_cap': data[coin]["quote"][currency]["market_cap"]
        }

    def price(self, coin, currency):
        result = self.manager.cryptocurrency_quotes_latest(symbol=coin, convert=currency)
        return self.filter_essential_data(result.data, coin=coin, currency=currency)
