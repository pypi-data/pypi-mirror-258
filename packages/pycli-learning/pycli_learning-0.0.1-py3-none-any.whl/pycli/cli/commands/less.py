import typer
import pydoc
from typing_extensions import Annotated

from ..utils.file import open_file


def handle(
    path: Annotated[str, typer.Argument()]
):
    with open_file(path) as f:
        pydoc.pager(f.read())
