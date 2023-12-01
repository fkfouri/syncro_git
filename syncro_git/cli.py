import shutil
import sys
import traceback
from os.path import dirname
from pathlib import Path

import click
from git import Repo  # pip install gitpython
from rich.console import Console



THIS_PATH = Path(dirname(sys.executable)) if getattr(sys, "frozen", False) else Path(dirname(__file__))
ROOT_PAHT = THIS_PATH.parents[0]

ORIGIN = "git@gitlab.gerdau.digital:analytics/databricks/dna-engineer-template.git"
DESTINY = "git@gitlab.ubirata.ai:templates_repo/gerdau_dna_engineer_template.git"
FOLDER_NAME = ".temp-dna-engineer-template"

ORIGIN = "git@gitlab.gerdau.digital:Industrial/gemeosupplychaintmecpin-lakehouse.git"
FOLDER_NAME = "gemeosupplychaintmecpin-lakehouse"
DESTINY = "git@gitlab.ubirata.ai:templates_repo/test.git"
DESTINY = "git@gitlab.ubirata.ai:tmec/lakehouse.git"

REMOTE_CLONE = "origin_clone"

console = Console(style="yellow")

@click.command()
@click.option("--origin", "-o", required=True, default=ORIGIN)
@click.option("--folder", "-f", required=True, default=FOLDER_NAME)
@click.option("--branch", "-b", required=False, default=None)
@click.option("--destiny", "-d", required=False, default=DESTINY)
def app(origin, folder, branch, destiny):
    target_dir = get_target_dir(folder)

    console.print(f"""
Path to be used as bridge: [purple]{folder}[/]
origin: [purple]{origin}[/]
{REMOTE_CLONE}: [purple]{destiny}[/] """)

    repo = None
    if target_dir.exists():
        try:
            repo = Repo(target_dir)
            console.print(f"Clone from [blue]{origin}[/b]")
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

    # tree = repo.head.commit.tree
    # log = []
    # log.append(git.remote("-v"))
    # log.append(git.branch('-v', '-a'))

    for branch in repo.branches:
        if 'feature' not in branch.name:
            refspec = "{}:{}".format(branch, branch)
            console.print(f"Push [bold blue]{branch}[/] to [bold blue]{REMOTE_CLONE}[/]")
            remote.push(refspec=refspec)

    console.print(":thumbs_up: Done !!!")



def get_target_dir(folder):
    if ".temp" not in folder.lower():
        folder = f".temp-{folder}"

    return ROOT_PAHT.joinpath(folder)


def get_all_branches(repo: Repo):
    """
    Clone the other branches as needed and setup them tracking the remote
    """
    for b in repo.remote(name="origin").fetch():
        try:
            console.print(f"Get branch from [bold blue]{b.name}[/]")
            repo.git.checkout("-B", b.name.split("/")[1], b.name)
        except: ...
    return repo


if __name__ == "__main__":
    app()
