import click
import locale
from eve.service import svc_crypto
from eve.config import DEFAULT_COIN, CURRENCY
from eve.utilities import utils as f


class Context:
    def __init__(self, coin, currency):
        self.coin = coin.upper()
        self.currency = currency.upper()
        self.crypto = svc_crypto.Crypto()


@click.group()
@click.option("-c", "--coin", type=str, help="Coin", default=DEFAULT_COIN, show_default=True)
@click.option("-ccy", "--currency", type=str, help="Currency", default=CURRENCY, show_default=True)
@click.pass_context
def cli(ctx, coin, currency):
    """Coin price for a given coin"""
    ctx.obj = Context(coin, currency)


@cli.command()
@click.pass_context
def price(ctx):
    """Price in another currency"""
    locale.setlocale(locale.LC_ALL, "")
    result = ctx.obj.crypto.price(coin=ctx.obj.coin, currency=ctx.obj.currency)
    price_value, price_currency = result["price"].split(" ")
    click.echo(f' {result["symbol"]} ({result["name"].upper()}) PRICE '.center(45, "="))
    click.echo(f'\U0001F4B1 Price:         {f.format_float_from_str(price_value, 4)} {price_currency}')
    click.echo(f'\U0001F4B0 Market cap:    {f.format_float_from_str(result["market_cap"], 4)} {price_currency}'),
    click.echo(f'\U0001F3E6 TTL supply:    {f.format_int_from_str(result["total_supply"])}')
    click.echo(f'\U0001F4C8 24H change:    {f.format_float_from_str(result["percent_change_24h"], 1)} %')
