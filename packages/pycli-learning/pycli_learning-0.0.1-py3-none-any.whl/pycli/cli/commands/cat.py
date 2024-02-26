import typer
from typing_extensions import Annotated

from ..utils.file import open_file


def handle(
    path: Annotated[str, typer.Argument()]
):
    with open_file(path) as f:
        print(f.read())
