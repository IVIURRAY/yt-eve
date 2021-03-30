import time
from datetime import datetime

import pytz


def convert_epoch_to(epoch, fmt):
    return time.strftime(fmt, time.localtime(epoch))


def is_around_midday(epoch):
    return 11 <= int(convert_epoch_to(epoch, "%H")) <= 13


def format_float_from_str(float_number: str, decimal_places: int):
    return f"{float(float_number):,.{decimal_places}f}"


def format_int_from_str(int_number: str):
    return f"{int(int_number):,d}"


def get_time_diff(date_one: str, date_two: str):
    return datetime.fromisoformat(date_one).astimezone(pytz.UTC) - datetime.fromisoformat(date_two).astimezone(
        pytz.UTC)
