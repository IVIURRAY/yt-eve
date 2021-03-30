import click

from eve.service import svc_cal


class Context:
    def __init__(self):
        self.calendar = svc_cal.Calendar()


@click.group()
@click.pass_context
def cli(ctx):
    """Google calendar interaction"""
    ctx.obj = Context()


@cli.command()
@click.pass_context
def events(ctx):
    """Display number of upcoming events in google calendar"""
    result = ctx.obj.calendar.next()
    for e in result:
        click.echo(f' {e["name"]} '.center(45, "="))
        click.echo(f'\U0001F468 Organizer:     {e["organizer"]}'),
        click.echo(f'\U000023F1  Starts in:     {e["starts_in"]}')
        click.echo(f'\U000023F3 Duration:      {e["duration"]}')
        click.echo(f'\U00002705 Status:        {e["status"]}')
