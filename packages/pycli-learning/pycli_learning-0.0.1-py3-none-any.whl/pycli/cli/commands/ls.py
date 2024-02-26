import typer
from typing_extensions import Annotated
from pathlib import Path
from rich.console import Console
from rich.columns import Columns

DIRECTORY_FORMAT = "[magenta][bold]{}"
FILE_FORMAT = "{}"

WITH_HIDDEN_GLOB_PATTERN = "*"
WITHOUT_HIDDEN_GLOB_PATTERN = "[!.]*"


def handle(
    path: Annotated[str, typer.Argument()] = ".",
    show_hidden: Annotated[bool, typer.Option()] = False
):
    files = __files_list__(path, show_hidden)
    columns = Columns(files, equal=True, expand=True)
    Console().print(columns)


def __files_list__(path: str, show_hidden: bool):
    glob_pattern = (
        WITH_HIDDEN_GLOB_PATTERN if show_hidden
        else WITHOUT_HIDDEN_GLOB_PATTERN
    )
    return [__format__(item) for item in Path(path).glob(glob_pattern)]


def __format__(file: Path):
    format_string = DIRECTORY_FORMAT if file.is_dir() else FILE_FORMAT
    return format_string.format(file.name)
