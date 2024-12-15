import pytest
from advent_of_code.day15.main import solve_part_one, solve_part_two


@pytest.mark.parametrize(
    "file_name, expected",
    [("input/day15/example2.txt", 2028), ("input/day15/example.txt", 10092)],
)
def test_solve_part_one(file_name: str, expected: int) -> None:
    assert solve_part_one(file_name=file_name) == expected


@pytest.mark.parametrize(
    "file_name, expected",
    [("input/day15/example.txt", 9021)],
)
def test_solve_part_two(file_name: str, expected: int) -> None:
    assert solve_part_two(file_name=file_name) == expected
