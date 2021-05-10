from pathlib import Path
import subprocess
import sys
import os
import json

import click

from typing import Dict, List

START_META = os.path.join(
    Path(os.path.dirname(__file__)).parent, "meta", "start")

LICENSES = os.path.join(START_META, "licenses")
TEMPLATES = os.path.join(START_META, "templates")


def get_langs_and_licenses() -> Dict[str, List[str]]:

    langs = [j.replace(".json", "")
             for j in [l for _, _, l in os.walk(TEMPLATES)][0]]

    lice = [j.replace(".txt", "")
            for j in [l for _, _, l in os.walk(LICENSES)][0]]

    return {"langs": langs, "lice": lice}


def check_virtual_env_installed() -> bool:
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    return "virtualenv" in installed_packages


class Start:

    def __init__(self) -> None:
        self.name: str = ""
        self.language: str = ""
        self.author: str = ""
        self.author_email: str = ""
        self.license: str = "mit"
        self.make_env: bool = False
        self.directory: str = "."
        self.git: bool = False

    def start_project(self) -> None:
        _license = os.path.join(START_META, "licenses", f"{self.license}.txt")
        template = os.path.join(START_META, "templates",
                                f"{self.language}.json")

        with open(template, "r") as f:
            data = json.load(f)

        for _file in data["create-files"]:
            self.create_file(_file)
            if _file in data["contents"]:
                contents = data["contents"][_file]
                if "{0}" in contents:
                    contents = contents.format(
                        self.name, self.author, self.author_email)  # check whether the text has format strings
                self.write_data(_file, contents)

        # add license
        try:
            with open(_license, "r") as f:
                self.write_data("LICENSE", f.read())
        except FileNotFoundError:
            pass
        # create all the required folders
        folders = {}
        folders[self.name] = data["create-src-folders"]["project-name"]
        self.create_src_directories(folders)

        if self.git:
            self.create_git_repo()
        if self.make_env:
            self.create_venv()

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

    def create_venv(self) -> None:
        if check_virtual_env_installed():
            subprocess.run(["virtualenv", os.path.join(
                self.directory, "env")], shell=True)
        else:
            click.echo(click.style(
                "virtualenv is not installed.", fg="yellow", bold=True))

    def create_git_repo(self) -> None:
        subprocess.run(["git", "init", self.directory], shell=True)


if __name__ == "__main__":
    check_virtual_env_installed()
