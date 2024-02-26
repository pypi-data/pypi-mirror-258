from unittest import mock
from pycli.cli.commands.mkdir import handle


@mock.patch('os.mkdir')
def test_mdkir(mock_mkdir):
    expected_path = 'test_folder/nested_folder'
    handle(expected_path)
    mock_mkdir.assert_called_with(expected_path, mock.ANY)
