import pytest

from advent_of_code.day5.main import get_middle_page_sum

@pytest.mark.parametrize("file_name, expected", [("input/day5/example.txt", 143)])
def test_middle_numbers_sum(file_name: str, expected: str) -> None:
  assert get_middle_page_sum(file_name=file_name) == expected