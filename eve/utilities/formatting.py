import time


def convert_epoch_to(epoch, fmt):
    return time.strftime(fmt, time.localtime(epoch))


def is_around_midday(epoch):
    return 11 <= int(convert_epoch_to(epoch, "%H")) <= 13


def format_float_from_str(float_number: str, decimal_places: int):
    return f"{float(float_number):,.{decimal_places}f}"


def format_int_from_str(int_number: str):
    return f"{int(int_number):,d}"
