import typer

from pycli.cli.commands import COMMANDS


class Cli():
    def __init__(self) -> None:
        self.app = typer.Typer()

    def run(self) -> None:
        self.__load_commands__()
        self.app()

    def __load_commands__(self) -> None:
        for name, handler in COMMANDS.items():
            self.app.command(name)(handler)
