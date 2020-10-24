import click

from eve.service import svc_football


class Context:
    def __init__(self):
        self.football = svc_football.Football()


@click.group()
@click.pass_context
def cli(ctx):
    """Football results"""
    ctx.obj = Context()


@cli.command()
@click.option(
    "-l",
    "--league",
    type=str,
    help="The league to view - See codes at https://github.com/openfootball/football.json",
    default="en.1",
)
@click.pass_context
def table(ctx, league):
    """View a table"""
    table = ctx.obj.football.table(league)
    for i, team in enumerate(table):
        rank = f"{i + 1}{pos_number(i+1)}:".center(6)
        name = f"{team['name']}".center(30)
        points = f"{team['points']} pts".center(6)
        stats = f"{team['gd']} gd".center(6)
        click.echo(f"{rank} {name} {points} {stats}")


def pos_number(pos):
    return {1: "st", 2: "nd", 3: "rd", 21: "st", 22: "nd", "23": "rd"}.get(pos, "th")
