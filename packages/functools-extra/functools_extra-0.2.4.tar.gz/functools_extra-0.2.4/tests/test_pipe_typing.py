# ruff: noqa: F841
from __future__ import annotations

from collections.abc import Generator, Iterable

from functools_extra import pipe


def add_one(x: int) -> int:
    return x + 1


def map_str(list_: Iterable[int]) -> Generator[str, None, None]:
    return (str(i) for i in list_)


def test_typing():
    integer: int = pipe(1, add_one)
    integer_false: str = pipe(1, *([add_one] * 10))  # type: ignore [assignment]


def test_typing_lists():
    int_list: list[int] = pipe(range(10), list)
    int_list_false: list[str] = pipe(range(10), list)  # type: ignore [arg-type]
    str_list: list[str] = pipe(range(10), map_str, list)
    str_list_false: list[int] = pipe(range(10), map_str, list)  # type: ignore [arg-type]
