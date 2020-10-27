import click

from eve.service import svc_github


class Context:
    def __init__(self):
        self.github = svc_github.GithubUtility()


@click.group()
@click.pass_context
def cli(ctx):
    """Github utilities"""
    ctx.obj = Context()


@cli.command()
@click.argument("name", type=str)
@click.option("-p", "--private", type=bool, help="Is the repo private?", default=False)
@click.option("-i", "--gitignore", type=str, help="The .gitignore file to add to the repo", default="")
@click.pass_context
def create(ctx, name, private, gitignore):
    """Create a github repo"""
    repo = ctx.obj.github.create_repo(name, private=private, gitignore=gitignore)
    click.echo(f"Created: {repo.name} at {repo.html_url}")
    click.echo("Run the below command to add the repo as a remote...")
    click.echo(f"git remote add origin {repo.clone_url}")


@cli.command()
@click.argument("name", type=str)
@click.pass_context
def delete(ctx, name):
    """Delete a github repo"""
    repo = ctx.obj.github.get_repo(name)
    if click.confirm(f"Are you sure you want to delete {repo.html_url}?", default=False):
        ctx.obj.github.delete_repo(repo.name)
        click.echo(f"Deleted: {repo.name}")
    else:
        click.echo(f"Aborted, did not delete: {repo.name}")
