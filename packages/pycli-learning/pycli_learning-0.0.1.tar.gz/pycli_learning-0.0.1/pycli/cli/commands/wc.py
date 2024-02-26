import typer
from typing_extensions import Annotated

from ..utils.file import open_file

OUTPUT_SEPARATOR = "         "


def handle(
    path: Annotated[str, typer.Argument()]
):
    with open_file(path) as f:
        lines, words, chars = map(str, __file_info__(f))
        print(OUTPUT_SEPARATOR.join([lines, words, chars, f.name]))


def __file_info__(f):
    lines = words = chars = 0
    for line in f:
        lines += 1
        words += len(line.split())
        chars += len(line)
    return lines, words, chars
