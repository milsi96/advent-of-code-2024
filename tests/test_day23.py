import pytest

from advent_of_code.day23.main import solve_part_one, solve_part_two


@pytest.mark.parametrize("file_name, expected", [("input/day23/example.txt", 7)])
def test_sove_part_one(file_name: str, expected: int) -> None:
    assert solve_part_one(file_name=file_name) == expected


@pytest.mark.parametrize(
    "file_name, expected", [("input/day23/example.txt", "co,de,ka,ta")]
)
def test_sove_part_two(file_name: str, expected: str) -> None:
    assert solve_part_two(file_name=file_name) == expected
