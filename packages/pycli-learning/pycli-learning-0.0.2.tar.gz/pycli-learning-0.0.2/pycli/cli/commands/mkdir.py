import os
from typing import Annotated

import typer


def handle(path: Annotated[str, typer.Argument()]):
    os.makedirs(path)
