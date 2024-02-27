from collections import deque
from typing import Annotated

import typer

from ..utils.file import open_file


def handle(
    path: Annotated[str, typer.Argument()],
    n: Annotated[int, typer.Option()] = 10,
):
    with open_file(path) as f:
        lines = "".join(deque(f, n))
        print(lines)
