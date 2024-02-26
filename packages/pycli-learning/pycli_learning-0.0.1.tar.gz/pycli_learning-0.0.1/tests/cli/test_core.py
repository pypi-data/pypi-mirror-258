import pytest
import typer
from unittest import mock
from pycli.cli.core import Cli

@pytest.fixture()
def app_mock():
    app = mock.create_autospec(typer.Typer)
    with mock.patch("typer.Typer", return_value=app):
        yield app


@mock.patch("pycli.cli.core.COMMANDS", {"test": "value"})
def test_Cli_run_with_commands(app_mock):
    Cli().run()
    app_mock.command.assert_called_with("test")
    app_mock.command().assert_called_with("value")
    app_mock.assert_called_once()
    
@mock.patch("pycli.cli.core.COMMANDS", {})
def test_Cli_run_without_commands(app_mock):
    Cli().run()
    app_mock.command.assert_not_called()
    app_mock.command().assert_not_called()
    app_mock.assert_called_once()
