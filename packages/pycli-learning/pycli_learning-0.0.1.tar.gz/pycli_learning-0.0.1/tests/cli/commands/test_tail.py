import pytest
from io import TextIOWrapper
from unittest import mock
from pycli.cli.commands.tail import handle


@pytest.fixture
def file_content():
    return ["First Line", "Second Line", "Third Line"]


@pytest.fixture
def file_mock(file_content):
    file = mock.create_autospec(TextIOWrapper)
    file.__enter__.return_value.__iter__.return_value = file_content
    return file


@mock.patch("pycli.cli.commands.tail.open_file")
def test_tail(mock_open, capfd, file_mock, file_content):
    mock_open.return_value = file_mock
    handle("test_folder/file", 2)
    out, _ = capfd.readouterr()
    mock_open.assert_called_with("test_folder/file")
    assert file_content[-2] in out
