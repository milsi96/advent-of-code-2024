import pytest

from advent_of_code.day24.main import solve_part_one


@pytest.mark.parametrize(
    "file_name, expected",
    [("input/day24/example.txt", 4), ("input/day24/example2.txt", 2024)],
)
def test_solve_part_one(file_name: str, expected: int) -> None:
    assert solve_part_one(file_name=file_name) == expected
