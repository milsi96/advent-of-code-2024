import pytest

from advent_of_code.day2.main import get_safe_reports, get_tolerated_safe_reports

@pytest.mark.parametrize("file_name, expected", [("input/day2/example.txt", 2)])
def test_safe_reports_number_is_correct(file_name: str, expected: int) -> None:
  assert get_safe_reports(file_name) == expected

@pytest.mark.parametrize("file_name, expected", [("input/day2/example.txt", 4)])
def test_tolerated_reports_number_is_correct(file_name: str, expected: int) -> None:
  assert get_tolerated_safe_reports(file_name) == expected
    