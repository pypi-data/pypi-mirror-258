from __future__ import annotations

from functools import reduce
from typing import Callable, TypeVar, overload

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
def pipe(value: T) -> T:
    ...


@overload
def pipe(value: T, func1: Callable[[T], T1]) -> T1:
    ...


@overload
def pipe(value: T, func1: Callable[[T], T1], func2: Callable[[T1], T2]) -> T2:
    ...


@overload
def pipe(
    value: T,
    func1: Callable[[T], T1],
    func2: Callable[[T1], T2],
    func3: Callable[[T2], T3],
) -> T3:
    ...


@overload
def pipe(
    value: T,
    func1: Callable[[T], T1],
    func2: Callable[[T1], T2],
    func3: Callable[[T2], T3],
    func4: Callable[[T3], T4],
) -> T4:
    ...


@overload
def pipe(
    value: T,
    func1: Callable[[T], T1],
    func2: Callable[[T1], T2],
    func3: Callable[[T2], T3],
    func4: Callable[[T3], T4],
    func5: Callable[[T4], T5],
) -> T5:
    ...


@overload
def pipe(
    value: T,
    func1: Callable[[T], T1],
    func2: Callable[[T1], T2],
    func3: Callable[[T2], T3],
    func4: Callable[[T3], T4],
    func5: Callable[[T4], T5],
    func6: Callable[[T5], T6],
) -> T6:
    ...


@overload
def pipe(
    value: T,
    func1: Callable[[T], T1],
    func2: Callable[[T1], T2],
    func3: Callable[[T2], T3],
    func4: Callable[[T3], T4],
    func5: Callable[[T4], T5],
    func6: Callable[[T5], T6],
    func7: Callable[[T6], T7],
) -> T7:
    ...


@overload
def pipe(
    value: T,
    func1: Callable[[T], T1],
    func2: Callable[[T1], T2],
    func3: Callable[[T2], T3],
    func4: Callable[[T3], T4],
    func5: Callable[[T4], T5],
    func6: Callable[[T5], T6],
    func7: Callable[[T6], T7],
    func8: Callable[[T7], T8],
) -> T8:
    ...


def pipe(
    value: T,
    func1: Callable[[T], T1] | None = None,
    func2: Callable[[T1], T2] | None = None,
    func3: Callable[[T2], T3] | None = None,
    func4: Callable[[T3], T4] | None = None,
    func5: Callable[[T4], T5] | None = None,
    func6: Callable[[T5], T6] | None = None,
    func7: Callable[[T6], T7] | None = None,
    func8: Callable[[T7], T8] | None = None,
) -> T | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8:
    funcs = (
        func
        for func in (func1, func2, func3, func4, func5, func6, func7, func8)
        if func is not None
    )
    return reduce(pipe_reduce, funcs, value)


def pipe_reduce(val, func):
    return func(val)
