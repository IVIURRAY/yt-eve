import time
import click

from eve.service import svc_weather


def convert_epoch_to(epoch, fmt):
    return time.strftime(fmt, time.localtime(epoch))


def is_around_midday(epoch):
    return 11 <= int(convert_epoch_to(epoch, "%H")) <= 13


class Context:
    def __init__(self, location):
        self.weather = svc_weather.Weather()
        self.location = location


@click.group()
@click.option("-l", "--location", type=str, help="Weather at this location.")
@click.pass_context
def cli(ctx, location):
    """Weather Information"""
    ctx.obj = Context(location)


@cli.command()
@click.pass_context
def current(ctx):
    """Current weather at a location"""
    result = ctx.obj.weather.current(location=ctx.obj.location)
    click.echo(f' {result["location"]} - {result["status"].upper()} '.center(45, "="))
    click.echo(f'\U0001F525 Temp: {result["temp"]} - {result["min"]}/{result["max"]} (min/max)')
    click.echo(f'\U0001F32A Wind: {round(result["wind"], 1)}')
    click.echo(f'\U0001F4A7 Rain: {result["rain"]}')
    click.echo(
        f'\U0001F315 Sunrise: {time.strftime("%H:%m", time.localtime(result["sun_rise"]))} - '
        f'Sunset: {time.strftime("%H:%m", time.localtime(result["sun_set"]))} \U0001F311'
    )


@cli.command()
@click.pass_context
def forecast(ctx):
    """Forecast for a location"""
    to_display = [wx for wx in ctx.obj.weather.forecast(location=ctx.obj.location) if is_around_midday(wx["time"])]

    def formatter(data):
        if isinstance(data, float):
            data = round(data, 2)
        return str(data).center(14)

    click.echo(f' {to_display[0]["location"]} '.center(int(14 * 5.5), "="))
    click.echo("\U0001F4C5 Date:" + "".join([formatter(convert_epoch_to(wx["time"], "%a %d %b")) for wx in to_display]))
    click.echo("\U0001F525 Temp:" + "".join([formatter(wx["temp"]) for wx in to_display]))
    click.echo("\U0001F32A Wind:" + "".join([formatter(wx["wind"]) for wx in to_display]))
    click.echo("\U0001F4A7 Rain:" + "".join([formatter(wx["rain"]) for wx in to_display]))
