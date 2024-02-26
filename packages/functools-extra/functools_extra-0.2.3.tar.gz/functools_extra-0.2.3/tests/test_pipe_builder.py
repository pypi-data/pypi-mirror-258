from functools_extra import pipe_builder


def test_empty_pipe_builder():
    pipe = pipe_builder()
    assert pipe(None) is None


def add_one(x: int) -> int:
    return x + 1


def test_pipe_builder():
    pipe = pipe_builder(add_one, lambda x: x * 2)
    assert pipe(1) == 4  # noqa: PLR2004
    assert pipe(2) == 6  # noqa: PLR2004
    assert pipe(1) == 4  # noqa: PLR2004
