from typing import List, Tuple
from advent_of_code.day13.main import Coordinate
from advent_of_code.day14.main import (
    Robot,
    get_quadrant,
    simulate_moves,
    solve_part_one,
)
import pytest


@pytest.mark.parametrize(
    "robot, expected",
    [
        (
            Robot(coordinate=(2, 4), velocity=(2, -3)),
            [(1, (4, 1)), (2, (6, 5)), (3, (8, 2)), (4, (10, 6)), (5, (1, 3))],
        )
    ],
)
def test_simulate_moves(robot: Robot, expected: List[Tuple[int, Coordinate]]) -> None:
    for seconds, coordinate in expected:
        assert (
            simulate_moves(robot=robot, seconds=seconds, height=7, width=11)
            == coordinate
        )


@pytest.mark.parametrize(
    "coordinate, quadrant",
    [
        ((6, 0), 2),
        ((9, 0), 2),
        ((1, 3), -1),
    ],
)
def test_get_quadrant(coordinate: Coordinate, quadrant: int) -> None:
    assert get_quadrant(coordinate=coordinate, height=7, width=11) == quadrant  # type: ignore


@pytest.mark.parametrize("file_name, expected", [("input/day14/example.txt", 12)])
def test_solve_part_one(file_name: str, expected: int) -> None:
    assert (
        solve_part_one(file_name=file_name, height=7, width=11, seconds=100) == expected
    )
