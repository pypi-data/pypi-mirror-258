from __future__ import annotations

from functools import reduce
from itertools import chain
from typing import Any, Callable, TypeVar, overload

T = TypeVar("T")
T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
T5 = TypeVar("T5")
T6 = TypeVar("T6")
T7 = TypeVar("T7")
T8 = TypeVar("T8")


@overload
def pipe_builder() -> Callable[[T], T]:
    ...


@overload
def pipe_builder(func1: Callable[[T], T1]) -> Callable[[T], T1]:
    ...


@overload
def pipe_builder(
    func1: Callable[[T], T1], func2: Callable[[T1], T2]
) -> Callable[[T], T2]:
    ...


@overload
def pipe_builder(
    func1: Callable[[T], T1],
    func2: Callable[[T1], T2],
    func3: Callable[[T2], T3],
) -> Callable[[T], T3]:
    ...


@overload
def pipe_builder(
    func1: Callable[[T], T1],
    func2: Callable[[T1], T2],
    func3: Callable[[T2], T3],
    func4: Callable[[T3], T4],
) -> Callable[[T], T4]:
    ...


@overload
def pipe_builder(
    func1: Callable[[T], T1],
    func2: Callable[[T1], T2],
    func3: Callable[[T2], T3],
    func4: Callable[[T3], T4],
    func5: Callable[[T4], T5],
) -> Callable[[T], T5]:
    ...


@overload
def pipe_builder(
    func1: Callable[[T], T1],
    func2: Callable[[T1], T2],
    func3: Callable[[T2], T3],
    func4: Callable[[T3], T4],
    func5: Callable[[T4], T5],
    func6: Callable[[T5], T6],
) -> Callable[[T], T6]:
    ...


@overload
def pipe_builder(
    func1: Callable[[T], T1],
    func2: Callable[[T1], T2],
    func3: Callable[[T2], T3],
    func4: Callable[[T3], T4],
    func5: Callable[[T4], T5],
    func6: Callable[[T5], T6],
    func7: Callable[[T6], T7],
) -> Callable[[T], T7]:
    ...


@overload
def pipe_builder(
    func1: Callable[[T], T1],
    func2: Callable[[T1], T2],
    func3: Callable[[T2], T3],
    func4: Callable[[T3], T4],
    func5: Callable[[T4], T5],
    func6: Callable[[T5], T6],
    func7: Callable[[T6], T7],
    func8: Callable[[T7], T8],
    *funcs: Callable[[T8], T8],
) -> Callable[[T], T8]:
    ...


@overload
def pipe_builder(
    func1: Callable[[T], T1],
    func2: Callable[[T1], T2],
    func3: Callable[[T2], T3],
    func4: Callable[[T3], T4],
    func5: Callable[[T4], T5],
    func6: Callable[[T5], T6],
    func7: Callable[[T6], T7],
    func8: Callable[[T7], T8],
    *funcs: Callable[[Any], Any],
) -> Callable[[T], Any]:
    ...


def pipe_builder(
    func1: Callable[[T], T1] | None = None,
    func2: Callable[[T1], T2] | None = None,
    func3: Callable[[T2], T3] | None = None,
    func4: Callable[[T3], T4] | None = None,
    func5: Callable[[T4], T5] | None = None,
    func6: Callable[[T5], T6] | None = None,
    func7: Callable[[T6], T7] | None = None,
    func8: Callable[[T7], T8] | None = None,
    *funcs: Callable[[Any], Any],
) -> Callable[[T], T | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 | Any]:
    def pipe(value: T) -> T | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 | Any:
        numbered_funcs = (
            func
            for func in (func1, func2, func3, func4, func5, func6, func7, func8)
            if func is not None
        )
        return reduce(pipe_reduce, chain(numbered_funcs, funcs), value)

    return pipe


def pipe_reduce(val, func):
    return func(val)
