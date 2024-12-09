import pytest

from advent_of_code.day9.main import get_checksum


@pytest.mark.parametrize("file_name, expected", [("input/day9/example.txt", 1928)])
def test_get_checksum(file_name: str, expected: int) -> None:
  assert get_checksum(file_name=file_name) == expected
