# Functools Extra
![PyPi](https://img.shields.io/pypi/v/functools-extra?color=%2334D058&label=pypi)
![Supported Python versions](https://img.shields.io/pypi/pyversions/functools-extra.svg?color=%2334D058)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Additional functional tools for python not covered in the [functools](https://docs.python.org/3/library/functools.html) library.

## Installation

```bash
pip install functools-extra

```

## How to use
### Pipes
A pipe is a function that takes a value and list of functions and calls them in order.
So `foo(bar(value))` is equivalent to `pipe(value, bar, foo)`.
You can use built-in functions like `list`, special operators from the [operator](https://docs.python.org/3/library/operator.html) module or custom functions.
All type-hints are preserved.
```python
from functools_extra import pipe
from operator import itemgetter

def add_one(x: int) -> int:
     return x + 1

assert pipe(range(3), list, itemgetter(2), add_one) == 3
```

Or you can use `pipe_builder` to create a reusable pipe:
```python
from functools_extra import pipe_builder

def add_one(x: int) -> int:
    return x + 1

def double(x: int) -> int:
    return x * 2

add_one_and_double = pipe_builder(add_one, double)
assert add_one_and_double(1) == 4
assert add_one_and_double(2) == 6
```

## Development
The project is built with [poetry](https://python-poetry.org/).
Check out the project and run
```bash
poetry install
```
to install the dependencies. After that you can run
```bash
poetry run pytest tests
```
to run the tests,
```bash
poetry run ruff format functools_extra tests --check
```
to check that the code is formatted correctly,
```bash
poetry run ruff format functools_extra tests
```
to format your code with ruff and
```bash
poetry run ruff check functools_extra tests
```
to lint the project.


## License

This project is licensed under the terms of the MIT license.
