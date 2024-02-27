# DOIPY

## Install

Simply run

```shell
$ pip install doipy
```

## Usage

This `doipy` package has two methods:

* `hello(name: str)`: say hello to the input name.
* `create(files: list[BinaryIO])`: loop through a list of files and do something.

To use it in the Command Line Interface, run:

```shell
$ doipy hello John
# Output of the hello command

$ doipy create file1 file2 file3
# Output of the create command
```

To use it in the Python code simply import it and call the exposed methods.

```python
from doipy import hello, create

hello(name='John')

with open('file1.txt', 'rb') as file1, open('file2.png', 'rb') as file2:
    create(files=[file1, file2])
```

## For developer

The project is managed by [Poetry](https://python-poetry.org/). Therefore, make sure that Poetry is installed in your
system. Then run

```shell
$ poetry install
```

to install all dependencies.

Then, install `doipy` package in editable mode. To do so, under the root directory, run:

```shell
$ pip install --editable .
```
