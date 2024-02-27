import pydoc
from typing import Annotated

import typer

from ..utils.file import open_file


def handle(path: Annotated[str, typer.Argument()]):
    with open_file(path) as f:
        pydoc.pager(f.read())
