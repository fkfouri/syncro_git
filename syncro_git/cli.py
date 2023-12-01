import shutil
import sys
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


@click.command()
@click.option("--origin", "-o", required=True, default=ORIGIN)
@click.option("--folder", "-f", required=True, default=FOLDER_NAME)
@click.option("--branch", "-b", required=False, default=None)
@click.option("--detiny", "-d", required=False, default=DESTINY)
def app(origin, folder, branch, detiny):
    if ".temp" not in folder.lower():
        folder = f".temp-{folder}"

    target_dir = ROOT_PAHT.joinpath(folder)

    if target_dir.exists():
        click.echo(f"Remove path {target_dir}")
        shutil.rmtree(target_dir)

    if branch is None:
        # Clone master
        repo = Repo.clone_from(url=origin, to_path=str(target_dir))

        # Clone the other branches as needed and setup them tracking the remote
        for b in repo.remote().fetch():
            repo.git.checkout("-B", b.name.split("/")[1], b.name)
    else:
        repo = Repo.clone_from(url=origin, to_path=str(target_dir), branch=branch, no_single_branch=True)

    branches = repo.branches
    branches = branches

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


if __name__ == "__main__":
    app()
