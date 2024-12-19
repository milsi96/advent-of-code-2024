import pytest

from advent_of_code.day19.main import solve_part_two
from advent_of_code.day19.main import solve_part_one


@pytest.mark.parametrize("file_name, expected", [("input/day19/example.txt", 6)])
def test_solve_part_one(file_name: str, expected: int) -> None:
    assert solve_part_one(file_name=file_name) == expected


@pytest.mark.parametrize("file_name, expected", [("input/day19/example.txt", 16)])
def test_solve_part_two(file_name: str, expected: int) -> None:
    assert solve_part_two(file_name=file_name) == expected
