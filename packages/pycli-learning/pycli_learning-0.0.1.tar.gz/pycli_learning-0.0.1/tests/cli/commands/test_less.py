import pytest
from io import TextIOWrapper
from unittest import mock
from pycli.cli.commands.less import handle


@pytest.fixture
def mocks():
    mock_file = mock.create_autospec(TextIOWrapper)
    file_content = mock.create_autospec(str)
    mock_file.__enter__.return_value.read.return_value = file_content
    return mock_file, file_content


@mock.patch("pydoc.pager")
@mock.patch("pycli.cli.commands.less.open_file")
def test_less(mock_open, mock_pager, mocks):
    mock_file, file_content = mocks
    mock_open.return_value = mock_file
    handle("test_folder/file")
    mock_open.assert_called_with("test_folder/file")
    mock_pager.assert_called_with(file_content)
