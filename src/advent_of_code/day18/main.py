from collections import defaultdict
from functools import partial
from heapq import heapify, heappop, heappush
import sys
from typing import DefaultDict, Dict, List, Tuple, TypeAlias

from advent_of_code.day16.main import COLUMN, ROW, Move
from advent_of_code.day16.main import Direction
from advent_of_code.utils.file_utils import process_file

Point: TypeAlias = Tuple[int, int]


def apply_direction(point: Point, direction: Direction) -> Point:
    return (point[ROW] + direction[ROW], point[COLUMN] + direction[COLUMN])


def get_next_moves(points: List[Point], current_position: Point) -> List[Move]:
    partial_add_direction = partial(apply_direction, current_position)
    return list(
        filter(
            lambda move: partial_add_direction(move.get_direction()) in points,
            [m for m in Move],
        )
    )


def dijkstra(
    maze: List[Point], start: Point, end: Point
) -> Tuple[DefaultDict[Point, int], List[Point]]:
    distances: DefaultDict[Point, int] = defaultdict(lambda: sys.maxsize)
    distances[start] = 0
    predecessor: Dict[Point, Point] = dict()
    priority_queue: List[Tuple[int, Point]] = [(0, start)]
    heapify(priority_queue)
    visited: set[Point] = set()

    while priority_queue:
        current_distance, current_node = heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node == end:
            break

        neighbors = [
            apply_direction(point=current_node, direction=move.get_direction())
            for move in get_next_moves(points=maze, current_position=current_node)
        ]

        for neighbor in neighbors:
            if neighbor in visited:
                continue

            tentative_distance = current_distance + 1

            if tentative_distance < distances[neighbor]:
                distances[neighbor] = tentative_distance
                predecessor[neighbor] = current_node
                heappush(priority_queue, (tentative_distance, neighbor))

    path = []
    if end in visited:
        current = end
        while current in predecessor.keys():
            path.append(current)
            current = predecessor[current]

        path.reverse()

    return distances, path


def get_maze(
    obstacles: List[Point], height: int, width: int
) -> Tuple[List[Point], Point, Point]:
    maze: List[Point] = list()

    for row in range(height + 1):
        for column in range(width + 1):
            if (row, column) not in obstacles:
                maze.append((row, column))

    return maze, (0, 0), (height, width)


def get_obstacles(file_name: str, limit: int) -> List[Point]:
    lines: List[List[int]] = process_file(
        file_name=file_name,
        process=lambda line: list(map(int, line.replace("\n", "").split(","))),
    )
    return list(map(lambda line: (line[COLUMN], line[ROW]), lines[:limit]))


def print_maze(
    points: List[Point], reindeer: Point, target: Point, path: List[Point]
) -> None:
    height = max(map(lambda p: p[ROW], points)) + 1
    width = max(map(lambda point: point[COLUMN], points)) + 1

    for i in range(height):
        line = ""
        for j in range(width):
            if (coord := (i, j)) == reindeer:
                line += "S"
            elif coord == target:
                line += "E"
            elif coord not in points:
                line += "#"
            elif coord in path:
                line += "O"
            else:
                line += "."
        print(line)


def solve_part_one(file_name: str, height: int, width: int, limit: int) -> int:
    maze, start, end = get_maze(
        obstacles=get_obstacles(file_name=file_name, limit=limit),
        height=height,
        width=width,
    )
    distances, _ = dijkstra(maze=maze, start=start, end=end)

    return distances[end]


def solve_part_two(file_name: str, height: int, width: int, limit: int) -> int:
    return 0


def main() -> None:
    file_name: str = "input/day18/input.txt"

    part_one = solve_part_one(file_name=file_name, height=70, width=70, limit=1024)
    print("Part one solution is", part_one)


if __name__ == "__main__":
    main()
