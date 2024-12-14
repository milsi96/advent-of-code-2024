from functools import partial, reduce
from itertools import groupby
from operator import mul
import re
from dataclasses import dataclass
from typing import List, Tuple, TypeAlias

from advent_of_code.utils.file_utils import process_file


Coordinate: TypeAlias = Tuple[int, int]
Velocity: TypeAlias = Tuple[int, int]

X = 0
Y = 1


@dataclass
class Robot:
    coordinate: Coordinate
    velocity: Velocity


def get_robots(file_name: str) -> List[Robot]:
    def parse_robot(line: str) -> Robot:
        robot_regex = r"p=(\d+),(\d+) v=(-*\d+),(-*\d+)"
        if (m := re.match(robot_regex, line)) is not None:
            groups = list(map(int, m.groups()))
            return Robot(
                coordinate=(groups[0], groups[1]), velocity=(groups[2], groups[3])
            )
        raise ValueError

    return process_file(file_name=file_name, process=parse_robot)


def visual_representation(
    height: int, width: int, coordinates: List[Coordinate]
) -> None:
    print()
    for i in range(height):
        line = ""
        for j in range(width):
            filtered_coords = list(filter(lambda c: c == (j, i), coordinates))
            line += "*" if len(filtered_coords) > 0 else " "
        print(line)
    print()


def simulate_moves(robot: Robot, seconds: int, width: int, height: int) -> Coordinate:
    new_x = robot.coordinate[X] + robot.velocity[X] * seconds
    new_y = robot.coordinate[Y] + robot.velocity[Y] * seconds
    return new_x % width, new_y % height


def get_quadrant(height: int, width: int, coordinate: Coordinate) -> int:
    mid_height, mid_width = (height - 1) / 2, (width - 1) / 2
    x, y = coordinate

    if 0 <= x < mid_width and 0 <= y < mid_height:
        return 0
    elif 0 <= x < mid_width and mid_height < y <= height:
        return 1
    elif mid_width < x <= width and 0 <= y < mid_height:
        return 2
    elif mid_width < x <= width and mid_height < y <= height:
        return 3

    return -1


def solve_part_one(file_name: str, height: int, width: int, seconds: int) -> int:
    robots = get_robots(file_name=file_name)
    new_coordinates = list(
        map(
            lambda robot: simulate_moves(
                robot=robot, seconds=seconds, width=width, height=height
            ),
            robots,
        )
    )
    get_quadrant_partial = partial(get_quadrant, height, width)
    quadrants = list(
        filter(lambda q: q != -1, map(get_quadrant_partial, new_coordinates))
    )
    return reduce(mul, [len(list(g)) for _, g in groupby(sorted(quadrants))])


def solve_part_two(file_name: str, height: int, width: int) -> int:
    robots = get_robots(file_name=file_name)
    i = 0
    while True:
        new_coordinates = list(
            map(
                lambda robot: simulate_moves(
                    robot=robot, seconds=i, width=width, height=height
                ),
                robots,
            )
        )
        distinct_coordinates = set(new_coordinates)
        if len(distinct_coordinates) == len(new_coordinates):
            visual_representation(
                coordinates=new_coordinates, height=height, width=width
            )
            break
        i += 1
    return i


def main() -> None:
    file_name: str = "input/day14/input.txt"

    part_one = solve_part_one(file_name=file_name, width=101, height=103, seconds=100)
    print("Part one solution is", part_one)

    part_two = solve_part_two(file_name=file_name, width=101, height=103)
    print("Part two solution is:", part_two)


if __name__ == "__main__":
    main()
