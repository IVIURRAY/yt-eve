import os

# Weather API
WX_API_KEY = os.environ.get("WX_API_KEY")
WX_LOCATION = os.environ.get("WX_LOCATION", "London")
WX_METRIC_TEMP = os.environ.get("WX_METRIC_TEMP", "celsius")
WX_METRIC_WIND = os.environ.get("WX_METRIC_WIND", "km_hour")

# Github API
GITHUB_USER = os.environ.get("GITHUB_USER")
GITHUB_PASS = os.environ.get("GITHUB_PASS")

# Tidy
TIDY_ROOT = os.environ.get("TIDY_ROOT", None)  # "</path/to/root>"

# Crypto
COIN_MARKET_CAP_API_KEY = os.environ.get("COIN_MARKET_CAP_API_KEY")
DEFAULT_COIN = os.environ.get("DEFAULT_COIN", "BTC")
CONVERT_TO_CURRENCY = os.environ.get("DESTINATION_CURRENCY", "GBP")
