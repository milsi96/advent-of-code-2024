from enum import StrEnum
from functools import partial
import sys
import time
from typing import List, Tuple, TypeAlias

from advent_of_code.utils.file_utils import process_file


Point: TypeAlias = Tuple[int, int]
Start: TypeAlias = Tuple[int, int]
End: TypeAlias = Tuple[int, int]

Direction: TypeAlias = Tuple[int, int]

ROW = 0
COLUMN = 1


class Move(StrEnum):
    UP = "up"
    LEFT = "left"
    RIGHT = "right"
    DOWN = "down"

    def get_direction(self) -> Direction:
        match self:
            case Move.UP:
                return (-1, 0)
            case Move.LEFT:
                return (0, 1)
            case Move.DOWN:
                return (1, 0)
            case Move.RIGHT:
                return (0, -1)


def apply_direction(point: Point, direction: Direction) -> Point:
    return (point[ROW] + direction[ROW], point[COLUMN] + direction[COLUMN])


def get_maze(file_name: str) -> Tuple[Start, End, List[Point]]:
    lines = process_file(
        file_name=file_name, process=lambda line: line.replace("\n", "")
    )
    points: List[Point] = list()
    start: Start
    end: End

    for row in range(len(lines)):
        for column in range(len(lines[row])):
            if lines[row][column] == ".":
                points.append((row, column))
            elif lines[row][column] == "S":
                points.append((row, column))
                start = (row, column)
            elif lines[row][column] == "E":
                end = (row, column)

    return start, end, points


def print_maze(
    points: List[Point], reindeer: Point, target: Point, path: List[Point]
) -> None:
    height = max(map(lambda p: p[ROW], points)) + 2
    width = max(map(lambda point: point[COLUMN], points)) + 2

    for i in range(height):
        line = ""
        for j in range(width):
            coord = (i, j)
            if coord == reindeer:
                line += "S"
            elif coord == target:
                line += "E"
            elif coord not in points:
                line += "#"
            elif coord in path:
                line += "°"
            else:
                line += "."
        print(line)


def get_next_moves(points: List[Point], current_position: Point) -> List[Move]:
    partial_add_direction = partial(apply_direction, current_position)
    return list(
        filter(
            lambda move: partial_add_direction(move.get_direction()) in points,
            [m for m in Move],
        )
    )


def find_best_path(points: List[Point], start: Start, end: End) -> int:
    def depth_first_search(
        target: Point, points: List[Point], current_point: Point, path: List[Point]
    ) -> int:
        print(path)
        print_maze(points=points, reindeer=current_point, target=end, path=path)
        print()

        if current_point == target:
            return 0

        new_points = list(
            filter(
                lambda point: point not in path,
                map(
                    lambda move: apply_direction(
                        point=current_point, direction=move.get_direction()
                    ),
                    get_next_moves(points=points, current_position=current_point),
                ),
            )
        )
        if len(new_points) == 0:
            return sys.maxsize

        time.sleep(0.5)

        return min(
            [
                1
                + depth_first_search(
                    target=target,
                    points=points,
                    current_point=point,
                    path=(path.copy() + [point]),
                )
                for point in new_points
            ]
        )

    return depth_first_search(
        target=end, points=points, current_point=start, path=[start]
    )


def solve_part_one(file_name: str) -> int:
    start, end, points = get_maze(file_name=file_name)

    find_best_path(points=points, start=start, end=end)

    return 0


def main() -> None:
    file_name: str = "input/day16/input.txt"

    part_one = solve_part_one(file_name=file_name)
    print("Part one solution is", part_one)

    # part_two = solve_part_two(file_name=file_name)
    # print("Part two solution is:", part_two)


if __name__ == "__main__":
    main()
