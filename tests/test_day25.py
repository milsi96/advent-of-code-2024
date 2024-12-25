from advent_of_code.day25.main import solve_part_one
import pytest


@pytest.mark.parametrize("file_name, expected", [("input/day25/example.txt", 3)])
def test_solve_part_one(file_name: str, expected: int) -> None:
    assert solve_part_one(file_name=file_name) == expected
