import pytest

from advent_of_code.day20.main import get_total_cheats


@pytest.mark.parametrize(
    "file_name, max_distance, limit, expected",
    [("input/day20/example.txt", 2, 0, 44), ("input/day20/example.txt", 20, 50, 285)],
)
def test_solve_part_one(
    file_name: str, max_distance: int, limit: int, expected: int
) -> None:
    assert (
        get_total_cheats(
            file_name=file_name, max_distance=max_distance, picoseconds_limit=limit
        )
        == expected
    )
