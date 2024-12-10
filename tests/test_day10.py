import pytest

from advent_of_code.day10.main import solve_part_one, solve_part_two

@pytest.mark.parametrize("file_name, expected", [("input/day10/example.txt", 36)])
def test_solve_part_one(file_name: str, expected: int) -> None:
  assert solve_part_one(file_name=file_name) == expected

@pytest.mark.parametrize("file_name, expected", [("input/day10/example.txt", 81)])
def test_solve_part_two(file_name: str, expected: int) -> None:
  assert solve_part_two(file_name=file_name) == expected