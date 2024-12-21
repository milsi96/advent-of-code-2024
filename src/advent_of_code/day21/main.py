from collections import defaultdict
from heapq import heapify, heappop, heappush
from itertools import product
import re
import sys
from typing import DefaultDict, Dict, List, Tuple
from advent_of_code.utils.file_utils import process_file
from advent_of_code.day18.main import Point, apply_direction, get_next_moves
from advent_of_code.day16.main import get_direction, Direction

A: str = "A"


def get_codes(file_name: str) -> List[str]:
    return process_file(
        file_name=file_name, process=lambda line: line.replace("\n", "")
    )


def get_numeric_keypad() -> Dict[str, Point]:
    return {
        "7": (0, 0),
        "8": (0, 1),
        "9": (0, 2),
        "4": (1, 0),
        "5": (1, 1),
        "6": (1, 2),
        "1": (2, 0),
        "2": (2, 1),
        "3": (2, 2),
        "0": (3, 1),
        "A": (3, 2),
    }


def get_directional_keypad() -> Dict[str, Point]:
    return {
        "^": (0, 1),
        "A": (0, 2),
        "<": (1, 0),
        "v": (1, 1),
        ">": (1, 2),
    }


def get_symbol_by_direction(direction: Direction) -> str:
    match direction:
        case (0, 1):
            return ">"
        case (0, -1):
            return "<"
        case (1, 0):
            return "v"
        case (-1, 0):
            return "^"
        case _:
            raise ValueError("This direction is unknown")


def dijkstra(
    maze: List[Point], start: Point, end: Point
) -> Tuple[DefaultDict[Point, int], List[List[Point]]]:
    distances: DefaultDict[Point, int] = defaultdict(lambda: sys.maxsize)
    distances[start] = 0
    predecessors: DefaultDict[Point, List[Point]] = defaultdict(list)
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

            if tentative_distance <= distances[neighbor]:
                distances[neighbor] = tentative_distance
                predecessors[neighbor].append(current_node)
                heappush(priority_queue, (tentative_distance, neighbor))

    def generate_paths(current: Point, path: List[Point]) -> List[List[Point]]:
        if current == start:
            return [[start] + path]
        paths = []
        for predecessor in predecessors[current]:
            paths.extend(generate_paths(predecessor, [current] + path))
        return paths

    all_paths = []
    if end in visited:
        all_paths = generate_paths(end, [])

    return distances, all_paths


def get_sequence(path: List[Point]) -> List[str]:
    result: List[str] = list()
    for i in range(len(path) - 1):
        result.append(get_symbol_by_direction(get_direction(path[i], path[i + 1])))
    return result


def combine_tuple(tuple: Tuple[str, str]) -> str:
    return tuple[0] + tuple[1]


def get_shortest_path(code: str, keypad: Dict[str, Point]) -> List[str]:
    code_coordinates = [keypad[A]] + list(map(lambda c: keypad[c], code))
    sequences: List[str] = list()
    for i in range(len(code_coordinates) - 1):
        _, paths = dijkstra(
            maze=list(keypad.values()),
            start=code_coordinates[i],
            end=code_coordinates[i + 1],
        )

        symbol_sequences = list(map(lambda p: "".join(get_sequence(p) + [A]), paths))

        if sequences == []:
            sequences = symbol_sequences
        else:
            combinations = list(product(sequences, symbol_sequences))
            sequences = list(map(combine_tuple, combinations))

    return sequences


def solve_part_one(file_name: str, directional_robots: int) -> int:
    codes = get_codes(file_name=file_name)
    numeric_keypad, directional_keypad = get_numeric_keypad(), get_directional_keypad()
    result = 0

    for code in codes:
        min_third_sequence_length = sys.maxsize
        third_sequence: str
        first_sequences = get_shortest_path(code=code, keypad=numeric_keypad)
        for first_sequence in first_sequences:
            second_sequences = get_shortest_path(
                code=first_sequence, keypad=directional_keypad
            )
            for second_sequence in second_sequences:
                third_sequence = min(
                    get_shortest_path(code=second_sequence, keypad=directional_keypad),
                    key=len,
                )
                min_third_sequence_length = min(
                    min_third_sequence_length, len(third_sequence)
                )

        result += min_third_sequence_length * int(re.sub("[^0-9]", "", code))

    return result


def main() -> None:
    file_name: str = "input/day21/input.txt"

    part_one = solve_part_one(file_name=file_name, directional_robots=2)
    print("Part one solution is", part_one)


if __name__ == "__main__":
    main()
