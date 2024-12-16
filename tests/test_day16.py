import pytest

from advent_of_code.day16.main import solve_part_one


@pytest.mark.parametrize(
    "file_name, expected",
    [
        # ("input/day16/example.txt", 7036),
        ("input/day16/example2.txt", 11048)
    ],
)
def test_solve_part_one(file_name: str, expected: int) -> None:
    assert solve_part_one(file_name=file_name) == expected
