import pytest

from advent_of_code.day6.main import get_distinct_positions

@pytest.mark.parametrize("file_name, expected", [("input/day6/example.txt", 41)])
def test_get_distinct_positions(file_name: str, expected: int) -> None:
  assert get_distinct_positions(file_name=file_name) == expected