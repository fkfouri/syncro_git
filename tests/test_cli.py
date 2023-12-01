from click.testing import CliRunner
from syncro_git import cli
import shutil
import pytest

@pytest.fixture(scope="session", autouse=True)
def clean_folders():
    for folder in cli.ROOT_PATH.iterdir():
        name = folder.stem
        if ".temp-" in name and folder.is_dir():
            shutil.rmtree(folder)



def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli.syncro, ["--help"])
    assert result.exit_code == 0 
    assert "This command will syncronize two git repositories" in result.output


def test_cli_template():
    runner = CliRunner()
    result = runner.invoke(cli.syncro, 
                           ["-o", "git@gitlab.gerdau.digital:analytics/databricks/dna-engineer-template.git",
                            "-d", "git@gitlab.ubirata.ai:templates_repo/gerdau_dna_engineer_template.git",
                            "--unit_test", True])

 
    assert result.exit_code == 0 
    assert "Done !!!" in result.output    


def test_exiting_folder():
    temp_folder = cli.ROOT_PATH.joinpath("temporary")
    temp_folder.mkdir(exist_ok=True)

    runner = CliRunner()
    result = runner.invoke(cli.syncro, 
                           ["-o", "git@gitlab.gerdau.digital:analytics/databricks/dna-engineer-template.git",
                            "-d", "git@gitlab.ubirata.ai:templates_repo/gerdau_dna_engineer_template.git",
                            "--folder", "temp_folder", 
                            "--unit_test", True])

    shutil.rmtree(temp_folder)
    assert result.exit_code == 0    