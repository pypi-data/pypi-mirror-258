import typer
import sys
import re
from typing_extensions import Annotated
from rich.console import Console

HIGHLIGHT_PATTERN = r"[red bold]\1[/red bold]"


def handle(
    search_str: Annotated[str, typer.Argument()]
):
    regexp_pattern = f"({search_str})"
    for line in sys.stdin:
        if re.search(search_str, line):
            __print_highlighted_line__(regexp_pattern, line)


def __print_highlighted_line__(regexp_pattern: str, line: str):
    console = Console(highlight=False)
    formatted_line = re.sub(regexp_pattern, HIGHLIGHT_PATTERN, line)
    console.print(formatted_line, end="")
