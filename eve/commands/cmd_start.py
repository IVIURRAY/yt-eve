from pathlib import Path
import os
import json

from typing import Dict, Union

import click

from eve.service.svc_start import Start, get_langs_and_licenses

START_META = os.path.join(
    Path(os.path.dirname(__file__)).parent, "meta", "start")

with open(os.path.join(START_META, "default.json"), "r") as f:
    data = json.load(f)


def get_default_values(collect: bool = False) -> Union[None, Dict[str, Dict[str, str]]]:
    # if collect is true then collect the info and store in default else return the default values
    if collect:
        req_fields = ["author", "author_email"]
        for r in req_fields:
            val = click.prompt(f"{r}")
            data["data"][r] = val

        with open(os.path.join(START_META, "default.json"), "w") as f:
            json.dump(data, f)

    else:
        return data


@click.command()
@click.option("-l", "--language", type=str, help="The language used in the project")
@click.option("-n", "--name", type=str, help="The name of the project")
@click.option("--license", type=str, help="The LICENSE to use", default="mit", show_default=True)
@click.option("-d", "--directory", type=str, help="The directory to create all the starter files and folders.", default=".", show_default=True)
@click.option("--env", help="Create a virtual env for Python projects", is_flag=True)
@click.option("--set-default", help="Add default values", is_flag=True)
@click.option("-y", type=bool, is_flag=True, help="Use default values while making the starter files.")
@click.option("--no-git", type=bool, is_flag=True, default=False, help="Do not initialize a git repo", show_default=False)
def cli(language: str, name: str, directory: str, license: str, y: bool, env: bool, set_default: bool, no_git: bool) -> None:
    """Start a new project in any language"""

    if not Path(directory).is_dir():
        click.echo(click.style(
            f"Directory {directory!r} does not exists.", fg="red", bold=True))
        return None

    if not set_default:
        langs_and_lice = get_langs_and_licenses()
        data = {"data": {"author": "", "author_email": ""}}
        if y:
            data = get_default_values()

        if name and language:
            if language in langs_and_lice["langs"]:
                if license not in langs_and_lice["lice"]:
                    click.echo(click.style(
                        "unrecognized license. Using MIT instead.", fg="yellow"))
                    click.echo(click.style(
                        f"Available Licenses: {langs_and_lice['lice']}"))

                start = Start()
                start.name = name
                start.author = data["data"]["author"]
                start.author_email = data["data"]["author_email"]
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

    else:
        get_default_values(collect=True)
