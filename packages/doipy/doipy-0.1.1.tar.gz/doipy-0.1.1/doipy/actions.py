from typing import BinaryIO
from rich import print


def create(files: list[BinaryIO]):
    print(':package: Create an [green]FDO[/green] for:')
    for file in files:
        print(f'  - {file.name}')


def hello(name: str):
    print(f'Hello {name}')
