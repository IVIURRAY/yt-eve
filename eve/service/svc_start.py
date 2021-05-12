from pathlib import Path
from ast import literal_eval
from datetime import date

import subprocess
import sys
import os
import json

from typing import Dict, List

# import click
import requests

from eve.config import AUTHOR_NAME, AUTHOR_EMAIL, GITHUB_USER

START_META = os.path.join(
    Path(os.path.dirname(__file__)).parent, "meta", "start")

LICENSES = os.path.join(START_META, "licenses")
TEMPLATES = os.path.join(START_META, "templates")


def get_license_list() -> List[str]:

    try:
        licenses = []
        contents = requests.get("https://api.github.com/licenses").json()
        for lic in contents:
            licenses.append(lic["key"])

        return licenses

    except requests.exceptions.ConnectionError:
        return []


def license_content(name: str) -> str:
    try:
        contents = requests.get(
            f"https://api.github.com/licenses/{name}").json()

        contents = contents["body"]
        contents = contents.replace("[year]", str(date.today().year))
        contents = contents.replace("[fullname]", GITHUB_USER)
        return contents

    except requests.exceptions.ConnectionError:
        return ""


def gitignore_contents(lang: str) -> str:
    try:
        contents = requests.get(
            f"https://api.github.com/gitignore/templates/{lang.capitalize()}").json()
        return contents["source"]

    except requests.exceptions.ConnectionError:
        return ""


def get_langs_and_licenses() -> Dict[str, List[str]]:

    langs = [j.replace(".json", "")
             for j in [l for _, _, l in os.walk(TEMPLATES)][0]]

    lice = get_license_list()

    return {"langs": langs, "lice": lice}


def check_virtual_env_installed() -> bool:
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    return "virtualenv" in installed_packages


class Start:

    def __init__(self) -> None:
        self.name: str = ""
        self.language: str = ""
        self.author: str = AUTHOR_NAME
        self.author_email: str = AUTHOR_EMAIL
        self.license: str = "mit"
        self.make_env: bool = False
        self.directory: str = "."
        self.git: bool = False

    def start_project(self) -> None:
        # load template
        self.template = os.path.join(START_META, "templates",
                                     f"{self.language}.json")

        with open(self.template, "r") as f:
            self.data = json.load(f)

        # create source tree
        tree = self.replace_project_name_src_directory()
        self.create_src_directories(tree)

        # add all the files
        for _file in self.data["create-files"]:
            _file = _file.replace("project-name", self.name)
            self.create_file(_file)

            # read the content of the file if available
            if _file in self.data["contents"]:
                contents = self.add_p_name_author_name_and_email(
                    self.data["contents"][_file])  # adds the project name, author name and email if possible.
                self.write_data(_file, contents)

        # add license and .gitignore
        self.add_license()
        self.add_gitignore()

        # initialize git and create the venv
        if self.git:
            self.create_git_repo()
        if self.make_env:
            self.create_venv()

    def add_license(self) -> None:
        contents = license_content(self.license)
        self.write_data("LICENSE", contents)

    def add_gitignore(self) -> None:
        contents = gitignore_contents(self.language)
        self.write_data(".gitignore", contents)

    def add_p_name_author_name_and_email(self, content: str) -> str:
        content = content.replace("##project--name##", self.name)
        content = content.replace("##author--name##", AUTHOR_NAME)
        content = content.replace("##author--email##", AUTHOR_EMAIL)
        return content

    def create_file(self, filename: str) -> None:
        Path(os.path.join(self.directory, filename)).touch()

    def write_data(self, filename: str, data: str) -> None:
        with open(os.path.join(self.directory, filename), "w") as f:
            f.write(data)

    def create_src_directories(self, dirs):
        for key, val in dirs.items():
            if isinstance(val, dict):
                for inner_key in val.keys():
                    Path(os.path.join(self.directory, key, inner_key)).mkdir(
                        parents=True, exist_ok=True)
                else:
                    # means no nested directories
                    Path(os.path.join(self.directory, key)).mkdir(
                        parents=True, exist_ok=True)

    def replace_project_name_src_directory(self):
        data = str(self.data["create-src-folders"])
        data = data.replace("project-name", self.name)
        return literal_eval(data)

    def create_venv(self) -> None:
        if check_virtual_env_installed():
            subprocess.run(["virtualenv", os.path.join(
                self.directory, "env")], shell=True)
        else:
            click.echo(click.style(
                "virtualenv is not installed.", fg="yellow", bold=True))

    def create_git_repo(self) -> None:
        subprocess.run(["git", "init", self.directory], shell=True)
