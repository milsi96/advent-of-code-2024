import pytest

from advent_of_code.day21.main import solve_part_one


@pytest.mark.parametrize(
    "file_name, directional_robots, expected", [("input/day21/example.txt", 2, 126384)]
)
def test_solve_part_one(file_name: str, directional_robots: int, expected: int) -> None:
    assert (
        solve_part_one(file_name=file_name, directional_robots=directional_robots)
        == expected
    )
