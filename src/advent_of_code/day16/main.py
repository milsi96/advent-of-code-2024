from collections import defaultdict
from enum import StrEnum
from functools import partial
from heapq import heapify, heappop, heappush
import sys
from typing import DefaultDict, Dict, List, Optional, Set, Tuple, TypeAlias

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
                points.append((row, column))
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
            if (coord := (i, j)) == reindeer:
                line += "S"
            elif coord == target:
                line += "E"
            elif coord not in points:
                line += " "
            elif coord in path:
                line += "O"
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


def get_direction(p1: Point, p2: Point) -> Direction:
    return (p2[0] - p1[0], p2[1] - p1[1])


def depth_first_search(
    target: Point,
    points: List[Point],
    current_point: Point,
    path: List[Point],
    score: int,
    best_score: int,
) -> Set[Point]:
    # print_maze(points=points, reindeer=current_point, target=target, path=path)
    # print()
    # time.sleep(0.1)

    if score > best_score:
        return set()

    if current_point == target:
        # comparing the first two elements to recognize if the reindeer rotated as first move
        final_score = score + (0 if get_direction(path[0], path[1]) == (0, 1) else 1000)
        if final_score > best_score:
            return set()
        print("Found a best path")
        return set(path)

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
        return set()

    def get_priority(path: List[Point], point: Point) -> int:
        if len(path) <= 2:
            return 1
        return (
            1
            if get_direction(p1=point, p2=path[-1])
            == get_direction(p1=path[-1], p2=path[-2])
            else 1001
        )

    priority = partial(get_priority, path)

    result: Set[Point] = set()
    for point in sorted(new_points, key=priority):
        seen_points = depth_first_search(
            target=target,
            points=points,
            current_point=point,
            path=(path.copy() + [point]),
            score=score + priority(point),
            best_score=best_score,
        )
        for s in seen_points:
            result.add(s)
    return result


def get_path_points(path: List[Point]) -> int:
    def direction(p1, p2):
        return (p2[0] - p1[0], p2[1] - p1[1])

    directions = [direction(path[i - 1], path[i]) for i in range(1, len(path))]

    turns = 0 if directions[0] != directions[1] else 1
    for i in range(1, len(directions)):
        if directions[i - 1] != directions[i]:
            turns += 1

    return len(path) - 1 + turns * 1000


def dijkstra(
    maze: List[Point], start: Point, end: Point
) -> Tuple[DefaultDict[Point, int], List[Point]]:
    distances: DefaultDict[Point, int] = defaultdict(lambda: sys.maxsize)
    distances[start] = 0
    predecessor: Dict[Point, Point] = dict()
    priority_queue: List[Tuple[int, Point, Optional[Tuple[int, int]]]] = [
        (0, start, None)
    ]
    heapify(priority_queue)
    visited: set[Point] = set()

    while priority_queue:
        current_distance, current_node, current_direction = heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node == end:
            break

        neighbors = [
            (
                apply_direction(point=current_node, direction=move.get_direction()),
                move.get_direction(),
            )
            for move in get_next_moves(points=maze, current_position=current_node)
        ]

        for neighbor, direction in neighbors:
            if neighbor in visited:
                continue

            tentative_distance = current_distance + (
                1
                if current_direction is None or current_direction == direction
                else 1001
            )

            if tentative_distance < distances[neighbor]:
                distances[neighbor] = tentative_distance
                predecessor[neighbor] = current_node
                heappush(priority_queue, (tentative_distance, neighbor, direction))

    path = []
    if end in visited:
        current = end
        while current in predecessor.keys():
            path.append(current)
            current = predecessor[current]

        path.reverse()

    return distances, path


def solve_part_one(file_name: str) -> int:
    start, end, points = get_maze(file_name=file_name)
    distances, path = dijkstra(maze=points, start=start, end=end)

    # print_maze(points=points, reindeer=start, target=end, path=path)

    return distances[end] + (0 if get_direction(path[0], path[1]) == (0, 1) else 1000)


def solve_part_two(file_name: str) -> int:
    # start, end, points = get_maze(file_name=file_name)
    # target_points = solve_part_one(file_name=file_name)

    # distinct_points = depth_first_search(target=end, points=points, current_point=start, path=[start], score=0, best_score=target_points)
    # print_maze(points=points, reindeer=start, target=end, path=list(distinct_points))
    return 0


def main() -> None:
    file_name: str = "input/day16/input.txt"

    part_one = solve_part_one(file_name=file_name)
    print("Part one solution is", part_one)

    part_two = solve_part_two(file_name=file_name)
    print("Part two solution is:", part_two)


if __name__ == "__main__":
    main()
