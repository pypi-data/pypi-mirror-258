from functools import partial
from operator import add, mul

import pytest
from functools_extra import pipe

add_one = partial(add, 1)
double = partial(mul, 2)


@pytest.mark.parametrize("num_funcs", range(9))
def test_pipe(num_funcs):
    assert pipe(0, *([add_one] * num_funcs)) == num_funcs


def test_pipe_with_args():
    num_funcs = 20
    assert pipe(0, *([add_one] * num_funcs)) == num_funcs


def test_numberic_pipe_to_str():
    conv_str = partial(map, str)
    map_add_one = partial(map, add_one)
    map_double = partial(map, double)
    assert pipe(range(5), map_add_one, map_double, conv_str, list) == [
        "2",
        "4",
        "6",
        "8",
        "10",
    ]
