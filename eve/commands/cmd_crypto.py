import click
import locale
from eve.service import svc_crypto
from eve.config import DEFAULT_COIN, CONVERT_TO_CURRENCY
from eve.utilities import formatting as f


class Context:
    def __init__(self, coin, destination_currency):
        self.coin = coin.upper()
        self.destination_currency = destination_currency.upper()
        self.crypto = svc_crypto.Crypto()


@click.group()
@click.option("-c", "--coin", type=str, help="Coin", default=DEFAULT_COIN, show_default=True)
@click.option("-d", "--destination-currency", type=str, help="destination", default=CONVERT_TO_CURRENCY, show_default=True)
@click.pass_context
def cli(ctx, coin, destination_currency):
    """Coin price for a given coin"""
    ctx.obj = Context(coin, destination_currency)


@cli.command()
@click.pass_context
def price(ctx):
    locale.setlocale(locale.LC_ALL, "")
    """Price in another currency"""
    result = ctx.obj.crypto.price(coin=ctx.obj.coin, destination_currency=ctx.obj.destination_currency)
    price_value, price_currency = result["price"].split(" ")
    click.echo(f' {result["symbol"]} ({result["name"].upper()}) PRICE'.center(45, "="))
    click.echo(f'\U0001F4B1 Price:         {f.format_float_from_str(price_value, 4)} {price_currency}')
    click.echo(f'\U0001F4B0 Market cap:    {f.format_float_from_str(result["market_cap"], 4)} {price_currency}'),
    click.echo(f'\U0001F3E6 TTL supply:    {f.format_int_from_str(result["total_supply"])}')
    click.echo(f'\U0001F4C8 24H change:    {f.format_float_from_str(result["percent_change_24h"], 1)} %')
