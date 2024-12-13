import pytest

from advent_of_code.day13.main import solve_part_one, solve_part_two


@pytest.mark.parametrize("file_name, expected", [("input/day13/example.txt", 480)])
def test_solve_part_one(file_name: str, expected: int) -> None:
    assert solve_part_one(file_name=file_name) == expected


@pytest.mark.parametrize(
    "file_name, expected", [("input/day13/example.txt", 875318608908)]
)
def test_solve_part_two(file_name: str, expected: int) -> None:
    assert solve_part_two(file_name=file_name) == expected
