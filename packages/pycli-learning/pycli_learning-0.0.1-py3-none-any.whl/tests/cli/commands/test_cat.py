import pytest
from io import TextIOWrapper
from unittest import mock
from pycli.cli.commands.cat import handle


@pytest.fixture
def file_content():
    return '''
        First Line
        Second Line
        Third Line
    '''


@pytest.fixture
def file_mock(file_content):
    file = mock.create_autospec(TextIOWrapper)
    file.__enter__.return_value.read.return_value = file_content
    return file


@mock.patch("pycli.cli.commands.cat.open_file")
def test_cat(mock_open, capfd, file_mock, file_content):
    mock_open.return_value = file_mock
    handle("test_folder/file")
    out, _ = capfd.readouterr()
    mock_open.assert_called_with("test_folder/file")
    assert file_content in out
