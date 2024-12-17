import pytest

from advent_of_code.day16.main import solve_part_one, solve_part_two


@pytest.mark.parametrize(
    "file_name, expected",
    [("input/day16/example.txt", 7036), ("input/day16/example2.txt", 11048)],
)
def test_solve_part_one(file_name: str, expected: int) -> None:
    assert solve_part_one(file_name=file_name) == expected


@pytest.mark.skip(reason="Day 16 part two is not implemented")
@pytest.mark.parametrize(
    "file_name, expected",
    [("input/day16/example.txt", 45), ("input/day16/example2.txt", 64)],
)
def test_solve_part_two(file_name: str, expected: int) -> None:
    assert solve_part_two(file_name=file_name) == expected
