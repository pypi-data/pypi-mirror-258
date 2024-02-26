import pytest
from io import TextIOWrapper
from unittest import mock
from pycli.cli.commands.wc import handle


@pytest.fixture
def file_content():
    return ["First Line", "Second Line", "Third Line"]


@pytest.fixture
def file_mock(file_content):
    file = mock.create_autospec(TextIOWrapper)
    file.__enter__.return_value.__iter__.return_value = file_content
    file.__enter__.return_value.name = "test_file"
    return file


@mock.patch("pycli.cli.commands.wc.open_file")
def test_wc(mock_open, capfd, file_mock):
    mock_open.return_value = file_mock
    handle("test_folder/file")
    out, _ = capfd.readouterr()
    mock_open.assert_called_with("test_folder/file")
    assert "6" in out
    assert "3" in out
    assert "test_file" in out
