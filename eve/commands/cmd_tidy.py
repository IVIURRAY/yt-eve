import collections
import os

import click

from eve.config import TIDY_ROOT


@click.command()
@click.option("-v", "--verbose", is_flag=True, type=bool, help="Enable verbose logging")
@click.option("-p", "--path", type=str, help="Directory path to tidy", default=TIDY_ROOT)
def cli(verbose, path):
    """Tidy a directory"""
    root_dir = path or os.path.join(os.path.expanduser("~"), "Downloads")

    file_mappings = collections.defaultdict()
    for filename in os.listdir(root_dir):
        if os.path.isfile(os.path.join(root_dir, filename)) and not filename.startswith("."):
            file_type = filename.split(".")[-1]
            file_mappings.setdefault(file_type, []).append(filename)

    for folder_name, folder_items in file_mappings.items():
        folder_path = os.path.join(root_dir, folder_name)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        if verbose:
            click.echo(f" Tidying {len(folder_items)} files in: {root_dir} ".center(100, "="))
        for folder_item in folder_items:
            source = os.path.join(root_dir, folder_item)
            destination = os.path.join(folder_path, folder_item)
            if verbose:
                click.echo(f"'{source.split('/')[-1]}' --> '/{'/'.join(destination.split('/')[-2:])}'")
            os.rename(source, destination)
