import click
from eve.service import svc_quote


class Context:
    def __init__(self, search):
        self.search = search
        self.quote = svc_quote.Quote()


@click.command()
@click.option('-s', '--search', type=str, help='Searchstring for random quotes.')
@click.pass_context
def cli(ctx, search):
    """Output quotes."""
    ctx.obj = Context(search)
    result = ctx.obj.quote.random(search=search)
    click.echo(result)
