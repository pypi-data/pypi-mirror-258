import pytest
from pathlib import Path
from unittest import mock
from pycli.cli.commands.ls import handle


@pytest.fixture
def glob_mock():
    with mock.patch("pathlib.Path.glob", autospec=True) as glob:
        yield glob


@pytest.fixture
def files():
    dir = mock.create_autospec(Path)
    file = mock.create_autospec(Path)
    dir.name = "directory"
    file.name = "file"
    return file, dir


def test_ls(capfd, glob_mock, files):
    glob_mock.return_value = files
    handle()
    out, _ = capfd.readouterr()
    assert files[0].name in out
    assert files[1].name in out


def test_ls_with_empty_results(capfd, glob_mock):
    glob_mock.return_value = []
    handle()
    out, _ = capfd.readouterr()
    assert not out
