import click
import locale
from eve.service import svc_crypto
from eve.config import DEFAULT_COIN, FIAT_CURRENCY
from eve.utilities import formatting as f


class Context:
    def __init__(self, coin, fiat):
        self.coin = coin
        self.fiat = fiat
        self.crypto = svc_crypto.Crypto()


@click.group()
@click.option("-c", "--coin", type=str, help="Coin", default=DEFAULT_COIN, show_default=True)
@click.option("-f", "--fiat", type=str, help="Fiat", default=FIAT_CURRENCY, show_default=True)
@click.pass_context
def cli(ctx, coin, fiat):
    """Coin price for a given coin"""
    ctx.obj = Context(coin, fiat)


@cli.command()
@click.pass_context
def price(ctx):
    locale.setlocale(locale.LC_ALL, "")
    """Current fiat price for a given coin"""
    result = ctx.obj.crypto.price(coin=ctx.obj.coin, fiat=ctx.obj.fiat)
    price_value, price_currency = result["price"].split(" ")
    click.echo(f' {result["symbol"]} - {result["name"].upper()} PRICE'.center(45, "="))
    click.echo(f'\U0001F4B6 Price:         {f.format_float_from_str(price_value, 4)} {price_currency}')
    click.echo(f'\U0001F4B0 TTL supply:    {f.format_int_from_str(result["total_supply"])}')
    click.echo(f'\U0001F4C8 24H change:   {f.format_float_from_str(result["percent_change_24h"], 1)} %')
