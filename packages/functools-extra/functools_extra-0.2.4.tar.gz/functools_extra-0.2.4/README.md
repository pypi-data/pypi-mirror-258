# Functools Extra
[![PyPi](https://img.shields.io/pypi/v/functools-extra?color=%2334D058&label=pypi)](https://pypi.org/project/functools-extra/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/functools-extra.svg?color=%2334D058)](https://pypi.org/project/functools-extra/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Rye](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/mitsuhiko/rye/main/artwork/badge.json)](https://rye-up.com/)

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
This project is using [Rye](https://rye-up.com/).
Check out the project and run
```bash
rye sync
```
to create a virtual environment and install the dependencies. After that you can run
```bash
rye run test
```
to run the tests,
```bash
rye run lint
```
to check the linting,
```bash
rye run fix
```
to format the project with ruff and fix the fixable errors.

## License

This project is licensed under the terms of the MIT license.
