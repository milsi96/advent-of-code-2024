import pytest

from advent_of_code.day23.main import solve_part_one


@pytest.mark.parametrize(
    "file_name, letter_filter, expected", [("input/day23/example.txt", "t", 7)]
)
def test_sove_part_one(file_name: str, letter_filter: str, expected: int) -> None:
    assert solve_part_one(file_name=file_name, letter_filter=letter_filter) == expected
