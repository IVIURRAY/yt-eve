from pathlib import Path
import os

import click

from eve.service.svc_start import Start, get_langs_and_licenses
from eve.config import AUTHOR_EMAIL, AUTHOR_NAME

START_META = os.path.join(
    Path(os.path.dirname(__file__)).parent, "meta", "start")


@click.command()
@click.option("-l", "--language", type=str, help="The language used in the project")
@click.option("-n", "--name", type=str, help="The name of the project")
@click.option("--license", type=str, help="The LICENSE to use", default="mit", show_default=True)
@click.option("-d", "--directory", type=str, help="The directory to create all the starter files and folders.", default=".", show_default=True)
@click.option("--env", help="Create a virtual env for Python projects", is_flag=True)
@click.option("--no-git", type=bool, is_flag=True, default=False, help="Do not initialize a git repo", show_default=False)
def cli(language: str, name: str, directory: str, license: str, env: bool, no_git: bool) -> None:
    """Start a new project in any language"""

    if not Path(directory).is_dir():
        click.echo(click.style(
            f"Directory {directory!r} does not exists.", fg="red", bold=True))
        return None

    langs_and_lice = get_langs_and_licenses()

    if name and language:
        if language in langs_and_lice["langs"]:
            if license.lower() not in langs_and_lice["lice"]:
                click.echo(click.style(
                    "unrecognized license. Using MIT instead.", fg="yellow"))
                click.echo(click.style(
                    f"Available Licenses: {langs_and_lice['lice']}"))

                license = "mit"

            start = Start()
            start.name = name
            start.author = AUTHOR_NAME
            start.author_email = AUTHOR_EMAIL
            start.directory = directory
            start.license = license
            start.make_env = env
            start.language = language
            start.git = not no_git
            start.start_project()

        else:
            click.echo(click.style("unrecognized language.", fg="red"))
            click.echo(click.style(
                f"Available languages: {langs_and_lice['langs']}"))

    else:
        click.echo(click.style(
            "Name and language are required.", fg="red"))
