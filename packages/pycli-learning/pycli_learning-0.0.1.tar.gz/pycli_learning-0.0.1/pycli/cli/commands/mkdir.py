import os
import typer
from typing_extensions import Annotated


def handle(
    path: Annotated[str, typer.Argument()]
):
    os.makedirs(path)
