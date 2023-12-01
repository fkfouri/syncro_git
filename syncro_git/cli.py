import shutil
import sys
import traceback
from os.path import dirname
from pathlib import Path

import click
from git import Repo  # pip install gitpython

THIS_PATH = Path(dirname(sys.executable)) if getattr(sys, "frozen", False) else Path(dirname(__file__))
ROOT_PAHT = THIS_PATH.parents[0]

ORIGIN = "git@gitlab.gerdau.digital:analytics/databricks/dna-engineer-template.git"
DESTINY = "git@gitlab.ubirata.ai:templates_repo/gerdau_dna_engineer_template.git"
FOLDER_NAME = ".temp-dna-engineer-template"

ORIGIN = "git@gitlab.gerdau.digital:Industrial/gemeosupplychaintmecpin-lakehouse.git"
FOLDER_NAME = "gemeosupplychaintmecpin-lakehouse"
DESTINY = "git@gitlab.ubirata.ai:templates_repo/test.git"

REMOTE_CLONE = "origin_clone"


@click.command()
@click.option("--origin", "-o", required=True, default=ORIGIN)
@click.option("--folder", "-f", required=True, default=FOLDER_NAME)
@click.option("--branch", "-b", required=False, default=None)
@click.option("--detiny", "-d", required=False, default=DESTINY)
def app(origin, folder, branch, detiny):
    target_dir = get_target_dir(folder)

    repo = None
    if target_dir.exists():
        try:
            click.echo(f"Read current path {target_dir}")
            repo = Repo(target_dir)
        except Exception as e:
            click.echo(f"It's not a valid path. The address '{target_dir}' will be recreated.")
            shutil.rmtree(target_dir)

    if repo is None:
        click.echo(f"Clone from {origin}")
        repo = Repo.clone_from(url=origin, to_path=str(target_dir), branch=branch)

    repo = get_all_branches(repo)
    git = repo.git

    branches = [r.name for r in repo.branches]
    remotes = [r.name for r in repo.remotes]
    heads = [r.path for r in repo.heads]

    if REMOTE_CLONE not in remotes:
        repo.create_remote(name=REMOTE_CLONE, url=detiny)
        remotes.append(REMOTE_CLONE)

    for remote in repo.remotes:
        remote.fetch()

    remote = repo.remote(name=REMOTE_CLONE)

    # tree = repo.head.commit.tree
    # log = []
    # log.append(git.remote("-v"))
    # log.append(git.branch('-v', '-a'))

    git.remote

    # remote.push()

    for branch in repo.branches:
        refspec = "{}:{}".format(branch, branch)
        click.echo(f"Push {refspec} to {DESTINY}")
        remote.push(refspec=refspec)

    repo = repo

    # if not target_dir.exists():
    #     click.echo("The target directory doesn't exist")
    #     raise SystemExit(1)

    # for entry in target_dir.iterdir():
    #     click.echo(f"{entry.name:{len(entry.name) + 5}}", nl=False)

    # click.echo()


# FOLDER = ROOT_PAHT.joinpath(FOLDER_NAME)
# if FOLDER.exists:
#     shutil.rmtree(FOLDER)

# FOLDER.mkdir(exist_ok=True)

#


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
            click.echo(f"Get branch from {b.name}")
            repo.git.checkout("-B", b.name.split("/")[1], b.name)
        except: ...
    return repo


if __name__ == "__main__":
    app()
