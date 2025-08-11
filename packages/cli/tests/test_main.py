from typer.testing import CliRunner

from udicti_cli.main import app

runner = CliRunner()


def test_welcome():
    result = runner.invoke(app, ["welcome"])
    assert result.exit_code == 0
    assert "Welcome to the UDICTI Developer CLI!" in result.stdout
