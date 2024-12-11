import pytest

from advent_of_code.day11.main import execute_cycles


@pytest.mark.parametrize(
    "file_name, times, expected",
    [
        ("input/day11/example.txt", 1, 7),
        ("input/day11/example2.txt", 6, 22),
        ("input/day11/example2.txt", 25, 55312),
    ],
)
def test_solve_part_one(file_name: str, times: int, expected: int) -> None:
    assert execute_cycles(file_name=file_name, cycles=times) == expected
