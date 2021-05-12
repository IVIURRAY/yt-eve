import os
import pathlib

# START API
AUTHOR_NAME = os.environ.get("AUTHOR_NAME", "")
AUTHOR_EMAIL = os.environ.get("AUTHOR_EMAIL", "")

# Weather API
WX_API_KEY = os.environ.get("WX_API_KEY", "<YOUR-API-KEY>")
WX_LOCATION = os.environ.get("WX_LOCATION", "<YOUR-DEFAULT-LOCATION>")
WX_METRIC_TEMP = os.environ.get(
    "WX_METRIC_TEMP", "<celsius|fahrenheit|kelvin>")
WX_METRIC_WIND = os.environ.get("WX_METRIC_WIND", "<miles_hour|km_hour|knots>")

# Github API
GITHUB_USER = os.environ.get("GITHUB_USER", "<USERNAME>")
GITHUB_PASS = os.environ.get("GITHUB_PASS", "<PASSWORD>")

# Tidy
TIDY_ROOT = os.environ.get("TIDY_ROOT", None)  # "</path/to/root>"

# Crypto
COIN_MARKET_CAP_API_KEY = os.environ.get(
    "COIN_MARKET_CAP_API_KEY", "<YOUR-API-KEY>")
DEFAULT_COIN = os.environ.get("DEFAULT_COIN", "<YOUR-DEFAULT-COIN>")
CURRENCY = os.environ.get("CURRENCY", "<YOUR-DEFAULT-CURRENCY>")

# Calendar
DEFAULT_CALENDAR_EVENTS_NUMBER = os.environ.get(
    "DEFAULT_EVENTS_NUMBER", "<YOUR-PREFERRED-NUMBER-OF-EVENTS-TO-DISPLAY>")
PATH_TO_CALENDAR_API_CRED = os.environ.get(
    "PATH_TO_CALENDAR_API_CRED", "<PATH-TO-GOOGLE-CALENDAR-API-CRED-DOT-JSON-FILE>"
)

# Quote Config
QU_SEARCH = "Tolkien"

# Note
NOTE_DEFAULT_PATH = os.path.join(pathlib.Path.home(), ".eve_note.json")
