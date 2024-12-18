import pytest

from advent_of_code.day18.main import solve_part_one, Point, solve_part_two


@pytest.mark.parametrize(
    "file_name, height, width, limit, expected",
    [("input/day18/example.txt", 6, 6, 12, 22)],
)
def test_solve_part_one(
    file_name: str, height: int, width: int, limit: int, expected: int
) -> None:
    assert (
        solve_part_one(file_name=file_name, height=height, width=width, limit=limit)
        == expected
    )


@pytest.mark.parametrize(
    "file_name, height, width, limit, expected",
    [("input/day18/example.txt", 6, 6, 12, (6, 1))],
)
def test_solve_part_two(
    file_name: str, height: int, width: int, limit: int, expected: Point
) -> None:
    assert (
        solve_part_two(file_name=file_name, height=height, width=width, limit=limit)
        == expected
    )
