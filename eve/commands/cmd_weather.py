import time

import click

from eve.service import svc_weather
from eve.utilities import formatting as f
from eve.config import WX_LOCATION


class Context:
    def __init__(self, location):
        self.weather = svc_weather.Weather()
        self.location = location


@click.group()
@click.option("-l", "--location", type=str, help="Weather at this location.", default=WX_LOCATION, show_default=True)
@click.pass_context
def cli(ctx, location):
    """Weather information"""
    ctx.obj = Context(location)


@cli.command()
@click.pass_context
def current(ctx):
    """Current weather at a location"""
    result = ctx.obj.weather.current(location=ctx.obj.location)
    click.echo(f' {result["location"]} - {result["status"].upper()} '.center(45, "="))
    click.echo(f'\U0001F525 Temp:    {result["temp"]} - {result["min"]}/{result["max"]} (min/max)')
    click.echo(f'\U0001F32A  Wind:    {round(result["wind"], 1)}')
    click.echo(f'\U0001F4A7 Rain:    {result["rain"] if result["rain"] else "No"}')
    click.echo(
        f'\U0001F315 Sunrise: {time.strftime("%H:%m", time.localtime(result["sun_rise"]))} - '
        f'Sunset: {time.strftime("%H:%m", time.localtime(result["sun_set"]))} \U0001F311'
    )


@cli.command()
@click.pass_context
def forecast(ctx):
    """Forecast for a location"""
    to_display = [wx for wx in ctx.obj.weather.forecast(location=ctx.obj.location) if f.is_around_midday(wx["time"])]

    def formatter(data):
        if isinstance(data, float):
            data = round(data, 2)
        return str(data).center(14)

    click.echo(f' {to_display[0]["location"]} '.center(int(14 * 5.5), "="))
    click.echo("\U0001F4C5 Date:" + "".join([formatter(f.convert_epoch_to(wx["time"], "%a %d %b")) for wx in to_display]))
    click.echo("\U0001F525 Temp:" + "".join([formatter(wx["temp"]) for wx in to_display]))
    click.echo("\U0001F32A  Wind:" + "".join([formatter(wx["wind"]) for wx in to_display]))
    click.echo("\U0001F4A7 Rain:" + "".join([formatter(wx["rain"] if wx["rain"] else "No") for wx in to_display]))
