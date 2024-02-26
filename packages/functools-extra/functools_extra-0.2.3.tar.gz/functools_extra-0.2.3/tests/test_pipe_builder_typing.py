# ruff: noqa: F841
from __future__ import annotations

from collections.abc import Generator, Iterable
from typing import Callable

from functools_extra import pipe_builder


def add_one(x: int) -> int:
    return x + 1


def map_str(list_: Iterable[int]) -> Generator[str, None, None]:
    return (str(i) for i in list_)


def test_typing():
    integer_pipe: Callable[[int], int] = pipe_builder(add_one)
    untyped_integer_pipe = pipe_builder(add_one)
    int_x: int = untyped_integer_pipe(1)
    str_x: str = untyped_integer_pipe(1)  # type: ignore [assignment]
    integer_pipe_false: Callable[[str], int] = pipe_builder(*([add_one] * 10))  # type: ignore [assignment]
    false_pipe = pipe_builder(add_one, map_str)  # type: ignore [misc]


def test_typing_lists():
    int_list_pipe = pipe_builder(list)
    int_list: list[int] = int_list_pipe(range(10))
    int_list_false: list[str] = int_list_pipe(range(10))  # type: ignore [arg-type]
    str_list_pipe: Callable[[Iterable[int]], list[str]] = pipe_builder(map_str, list)
    str_list: list[str] = str_list_pipe(range(10))
    str_list_false: list[int] = str_list_pipe(range(10))  # type: ignore [assignment]
