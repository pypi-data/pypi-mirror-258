import pytest
import io
from unittest import mock
from pycli.cli.commands.grep import handle


@pytest.fixture(autouse=True)
def stdin_mock():
    with mock.patch("sys.stdin") as stdin:
        stdin.__iter__.return_value = io.StringIO("Lorem Ipsum")
        yield stdin


def test_grep(capfd):
    handle("Lo")
    out, _ = capfd.readouterr()
    assert "Lorem Ipsum" in out


def test_grep_with_empty_results(capfd):
    handle("Empty")
    out, _ = capfd.readouterr()
    assert not out
