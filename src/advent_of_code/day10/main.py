from functools import reduce
from typing import Dict, List, Set, Tuple, TypeAlias

from advent_of_code.utils.file_utils import process_file

Coordinate: TypeAlias = Tuple[int, int]

X = 0
Y = 1


def next_move(
    input: Dict[Coordinate, int], current_point: Coordinate
) -> Set[Coordinate]:
    new_moves = {
        (current_point[X] - 1, current_point[Y]),
        (current_point[X] + 1, current_point[Y]),
        (current_point[X], current_point[Y] + 1),
        (current_point[X], current_point[Y] - 1),
    }

    result = set(
        filter(
            lambda move: move in input.keys()
            and input[move] - input[current_point] == 1,
            new_moves,
        )
    )
    return result


def _trigger_next_move(
    input: Dict[Coordinate, int], path: List[Coordinate], next_move: Coordinate
) -> List[Coordinate]:
    new_path = path.copy()
    new_path.append(next_move)
    return get_trailheads(input=input, path=new_path)


def get_trailheads(
    input: Dict[Coordinate, int], path: List[Coordinate]
) -> List[Coordinate]:
    current_point: Coordinate = path[-1]
    if input.get(current_point) == 9:
        return [current_point]

    next_moves = next_move(input=input, current_point=current_point)
    if len(next_moves) == 0:
        return []

    return reduce(
        _reduce_list,
        [
            _trigger_next_move(input=input, path=path, next_move=move)
            for move in next_moves
        ],
    )


def _reduce_list(a, b) -> List[Coordinate]:
    a.extend(b)
    return a


def solve_part_one(file_name: str) -> int:
    lines = process_file(
        file_name=file_name, process=lambda line: line.replace("\n", "")
    )
    input: Dict[Coordinate, int] = dict()
    for row in range(len(lines)):
        for column in range(len(lines[row])):
            input[(row, column)] = int(lines[row][column])

    start_points: Set[Coordinate] = set(
        map(lambda entry: entry[0], filter(lambda entry: entry[1] == 0, input.items()))
    )

    result = {
        start: set(
            reduce(
                _reduce_list,
                [_trigger_next_move(input=input, path=[], next_move=start)],
            )
        )
        for start in start_points
    }

    return len([coord for value in result.values() for coord in value])


def solve_part_two(file_name: str) -> int:
    lines = process_file(
        file_name=file_name, process=lambda line: line.replace("\n", "")
    )
    input: Dict[Coordinate, int] = dict()
    for row in range(len(lines)):
        for column in range(len(lines[row])):
            input[(row, column)] = int(lines[row][column])

    start_points: Set[Coordinate] = set(
        map(lambda entry: entry[0], filter(lambda entry: entry[1] == 0, input.items()))
    )

    result = {
        start: reduce(
            _reduce_list, [_trigger_next_move(input=input, path=[], next_move=start)]
        )
        for start in start_points
    }

    return len([coord for value in result.values() for coord in value])


def main() -> None:
    file_name: str = "input/day10/input.txt"

    part_one = solve_part_one(file_name=file_name)
    print("Part one solution is:", part_one)

    part_two = solve_part_two(file_name=file_name)
    print("Part two solution is:", part_two)


if __name__ == "__main__":
    main()
