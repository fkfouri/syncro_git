import os
import shutil
import sys
import traceback
from os.path import dirname
from pathlib import Path

import click
from git import Repo  # pip install gitpython
from rich.console import Console

ROOT_PATH = Path(os.getcwd())
REMOTE_CLONE = "origin_clone"


# ORIGIN = "git@gitlab.gerdau.digital:analytics/databricks/dna-engineer-template.git"
# DESTINY = "git@gitlab.ubirata.ai:templates_repo/gerdau_dna_engineer_template.git"


# ORIGIN = "git@gitlab.gerdau.digital:Industrial/gemeosupplychaintmecpin-lakehouse.git"
# FOLDER_NAME = "gemeosupplychaintmecpin-lakehouse"
# DESTINY = "git@gitlab.ubirata.ai:templates_repo/test.git"
# DESTINY = "git@gitlab.ubirata.ai:tmec/lakehouse.git"


console = Console(style="yellow")


@click.command()
@click.option("--origin", "-o", required=True, default=None)
@click.option("--destiny", "-d", required=True, default=None)
@click.option("--folder", "-f", required=False, default=None)
@click.option("--branch", "-b", required=False, default=None)
@click.option("--unit_test", required=False, default=False, type=bool)
def syncro_git(origin, folder, branch, destiny, unit_test):
    """This command will syncronize two git repositories"""
    folder = get_folder(folder, origin)
    target_dir = get_target_dir(folder)

    console.print(f"""
Path to be used as bridge: [purple]{folder}[/]
origin: [purple]{origin}[/]
{REMOTE_CLONE}: [purple]{destiny}[/]
WORK_DIR: [purple]{target_dir}[/]
 """)

    repo = None
    if target_dir.exists():
        try:
            console.print(f"Reading the target_dir [blue]{target_dir}[/]")
            repo = Repo(target_dir)
        except Exception as e:
            console.print(f"It's not a valid path. The address [red]{target_dir}[/] will be recreated.", style="red")
            shutil.rmtree(target_dir)

    if repo is None:
        console.print(f"Clone from [blue]{origin}[/]")
        repo = Repo.clone_from(url=origin, to_path=str(target_dir), branch=branch)

    repo = get_all_branches(repo)
    git = repo.git

    branches = [r.name for r in repo.branches]
    remotes = [r.name for r in repo.remotes]
    heads = [r.path for r in repo.heads]

    if REMOTE_CLONE not in remotes:
        repo.create_remote(name=REMOTE_CLONE, url=destiny)
        remotes.append(REMOTE_CLONE)

    for remote in repo.remotes:
        remote.fetch()

    remote = repo.remote(name=REMOTE_CLONE)

    if not unit_test:  # pragma: no cover
        for branch in repo.branches:
            if "feature" not in branch.name:
                refspec = "{}:{}".format(branch, branch)
                console.print(f"Push [bold blue]{branch}[/] to [bold blue]{REMOTE_CLONE}[/]")
                remote.push(refspec=refspec)

    console.print(":thumbs_up: Done !!!")


def get_folder(folder, origin):
    if folder is None:
        folder = origin.split("/")[-1].replace(".git", "")

    return folder


def get_target_dir(folder):
    if ".temp" not in folder.lower():
        folder = f".temp-{folder}"

    return ROOT_PATH.joinpath(folder)


def get_all_branches(repo: Repo):
    """
    Clone the other branches as needed and setup them tracking the remote
    """
    for b in repo.remote(name="origin").fetch():
        try:
            console.print(f"Get branch from [bold blue]{b.name}[/]")
            repo.git.checkout("-B", b.name.split("/")[1], b.name)
        except:  # pragma: no cover
            ...
    return repo


if __name__ == "__main__":  # pragma: no cover
    syncro_git()
