import contextlib
import sys

ERROR_TYPES = {
    FileNotFoundError: "No such file or directory: '{filename}'",
    IsADirectoryError: "Is a directory: '{filename}'"
}


@contextlib.contextmanager
def open_file(path: str):
    try:
        with open(path) as file:
            yield file
    except OSError as err:
        __handle_error__(err)


def __handle_error__(err: OSError):
    error_message = ERROR_TYPES.get(err.__class__, err.__str__())
    print(
        error_message.format(filename=err.filename)
    )
    sys.exit(err.errno)
