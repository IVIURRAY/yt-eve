import os

# Weather API
WX_API_KEY = os.environ.get("WX_API_KEY", "<YOUR-API-KEY>")
WX_LOCATION = os.environ.get("WX_LOCATION", "<YOUR-DEFAULT-LOCATION>")
WX_METRIC_TEMP = os.environ.get("WX_METRIC_TEMP", "<celsius|fahrenheit|kelvin>")
WX_METRIC_WIND = os.environ.get("WX_METRIC_WIND", "<miles_hour|km_hour|knots>")

# Github API
GITHUB_USER = os.environ.get("GITHUB_USER", "<USERNAME>")
GITHUB_PASS = os.environ.get("GITHUB_PASS", "<PASSWORD>")

# Tidy
TIDY_ROOT = os.environ.get("TIDY_ROOT", None)  # "</path/to/root>"

# Crypto
COIN_MARKET_CAP_API_KEY = os.environ.get("COIN_MARKET_CAP_API_KEY", "<YOUR-API-KEY>")
DEFAULT_COIN = os.environ.get("DEFAULT_COIN", "<YOUR-DEFAULT-COIN>")
CURRENCY = os.environ.get("CURRENCY", "<YOUR-DEFAULT-CURRENCY>")
