import pytest
from click.testing import CliRunner

from eve.commands.cmd_crypto import cli
from eve.config import DEFAULT_COIN, CURRENCY


@pytest.fixture
def runner():
    return CliRunner()


def test_price_returned_with_default_options(runner):
    result = runner.invoke(cli, ["price"])
    title, price, market_cap, total_supply, daily_change, _ = tuple(result.output.split("\n"))
    assert not result.exception
    assert DEFAULT_COIN in title
    assert CURRENCY in price
    assert len(total_supply) > 1
    assert len(daily_change) > 1


def test_price_returned_in_supplied_target_currency(runner):
    target_fiat_currency = "GBP"
    result = runner.invoke(cli, ["-ccy", target_fiat_currency, "price"])
    price = tuple(result.output.split("\n"))[2]
    assert not result.exception
    assert target_fiat_currency in price


def test_explicit_coin_supply(runner):
    supplied_coin = "ETH"
    result = runner.invoke(cli, ["-c", supplied_coin, "price"])
    title = tuple(result.output.split("\n"))[0]
    assert not result.exception
    assert supplied_coin in title
