import pytest
from advent_of_code.day8.main import get_all_antinodes, get_first_level_antinodes


@pytest.mark.parametrize("file_name, expected", [("input/day8/example.txt", 14)])
def test_get_first_level_antinodes(file_name: str, expected: int) -> None:
    assert get_first_level_antinodes(file_name=file_name) == expected


@pytest.mark.parametrize(
    "file_name, expected",
    [("input/day8/example.txt", 34), ("input/day8/example2.txt", 9)],
)
def test_get_all_antinodes(file_name: str, expected: int) -> None:
    assert get_all_antinodes(file_name=file_name) == expected
