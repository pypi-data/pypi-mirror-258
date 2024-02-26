def test_readme_pipe():
    from operator import itemgetter

    from functools_extra import pipe

    def add_one(x: int) -> int:
        return x + 1

    assert pipe(range(3), list, itemgetter(2), add_one) == 3  # noqa: PLR2004


def test_readme_pipe_builder():
    from functools_extra import pipe_builder

    def add_one(x: int) -> int:
        return x + 1

    def double(x: int) -> int:
        return x * 2

    add_one_and_double = pipe_builder(add_one, double)
    assert add_one_and_double(1) == 4  # noqa: PLR2004
    assert add_one_and_double(2) == 6  # noqa: PLR2004
