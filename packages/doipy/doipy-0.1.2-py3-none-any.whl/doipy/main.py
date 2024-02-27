import typer
from typing import Annotated

from doipy.actions import create, hello

app = typer.Typer()


@app.command(name='create')
def create_command(files: Annotated[list[typer.FileBinaryRead], typer.Argument(help='A list of files for an FDO.')]):
    """Create a new FDO from input files."""
    create(files)


@app.command(name='hello')
def hello_command(name: Annotated[str, typer.Argument(help='The name to greet.')]):
    """Greet the person"""
    hello(name)


if __name__ == '__main__':
    app()
