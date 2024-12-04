import pytest

from advent_of_code.day4.main import get_total_X, get_total_occurrences

@pytest.mark.parametrize("file_name, word, expected", [("input/day4/example.txt", "XMAS", 18)])
def test_find_occurrence(file_name: str, word: str, expected: int) -> None:
  assert get_total_occurrences(file_name=file_name, word=word) == expected


@pytest.mark.parametrize("file_name, word, expected", [("input/day4/example.txt", "MAS", 9)])
def test_find_X(file_name: str, word: str, expected: int) -> None:
  assert get_total_X(file_name=file_name, word=word) == expected
