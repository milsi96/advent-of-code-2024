from concurrent.futures import Future, ProcessPoolExecutor
from dataclasses import dataclass
from enum import StrEnum
from typing import Generator, List, Tuple
from advent_of_code.utils.file_utils import process_file


class Direction(StrEnum):
    UP = "up"
    DOWN = "down"
    RIGHT = "right"
    LEFT = "left"


@dataclass
class Position:
    row: int
    column: int


def _move(
    obstacles: List[Position], current_position: Position, direction: Direction
) -> Tuple[Position, Direction]:
    match direction:
        case Direction.UP:
            next_position = Position(current_position.row - 1, current_position.column)
            while next_position in obstacles:
                return _move(
                    obstacles=obstacles,
                    current_position=current_position,
                    direction=Direction.RIGHT,
                )
            return (next_position, Direction.UP)
        case Direction.RIGHT:
            next_position = Position(current_position.row, current_position.column + 1)
            while next_position in obstacles:
                return _move(
                    obstacles=obstacles,
                    current_position=current_position,
                    direction=Direction.DOWN,
                )
            return (next_position, Direction.RIGHT)
        case Direction.DOWN:
            next_position = Position(current_position.row + 1, current_position.column)
            while next_position in obstacles:
                return _move(
                    obstacles=obstacles,
                    current_position=current_position,
                    direction=Direction.LEFT,
                )
            return (next_position, Direction.DOWN)
        case Direction.LEFT:
            next_position = Position(current_position.row, current_position.column - 1)
            while next_position in obstacles:
                return _move(
                    obstacles=obstacles,
                    current_position=current_position,
                    direction=Direction.UP,
                )
            return (next_position, Direction.LEFT)
        case default:
            raise ValueError("This direction is unknown:", default)


def _get_route(
    obstacles: List[Position], borders: List[Position], current_position: Position
) -> List[Position]:
    direction = Direction.UP
    distinct_positions: List[Position] = [current_position]
    while current_position not in borders:
        next_position, direction = _move(
            obstacles=obstacles, current_position=current_position, direction=direction
        )
        if next_position not in distinct_positions:
            distinct_positions.append(next_position)
        current_position = next_position

    return distinct_positions


def _parse_map(map: List[List[str]]) -> Tuple[List[Position], Position, List[Position]]:
    current_position: Position
    obstacles: List[Position] = []
    for row in range(len(map)):
        for column in range(len(map[row])):
            if map[row][column] == "^":
                current_position = Position(row, column)
            elif map[row][column] == "#":
                obstacles.append(Position(row, column))

    assert len(map) == len(map[0])
    map_size = len(map)
    borders = [Position(row=row, column=0) for row in range(map_size)]
    borders.extend([Position(row=row, column=map_size - 1) for row in range(map_size)])
    borders.extend([Position(row=0, column=column) for column in range(map_size)])
    borders.extend(
        [Position(row=map_size - 1, column=column) for column in range(map_size)]
    )
    return (obstacles, current_position, borders)


def get_distinct_positions(file_name: str) -> int:
    map: List[List[str]] = process_file(
        file_name=file_name, process=lambda x: [c for c in x.replace("\n", "")]
    )
    obstacles, current_position, borders = _parse_map(map=map)
    distinct_positions: List[Position] = _get_route(
        obstacles=obstacles, borders=borders, current_position=current_position
    )
    return len(distinct_positions)


def generate_new_obstacles(
    obstacles: List[Position], possible_obstacles: List[Position]
) -> Generator[List[Position], None, None]:
    print("New possible obstacles are:", len(possible_obstacles))
    for po in possible_obstacles:
        obstacles_copy = obstacles.copy()
        obstacles_copy.append(po)
        yield obstacles_copy


def _task(
    obstacles: List[Position],
    borders: List[Position],
    initial_position: Position,
    run: int,
) -> int:
    print("Task number:", run)
    direction = Direction.UP
    current_position = initial_position
    distinct_positions: List[Tuple[Position, Direction]] = [
        (current_position, direction)
    ]
    while current_position not in borders:
        next_position, direction = _move(
            obstacles=obstacles, current_position=current_position, direction=direction
        )
        if (next_position, direction) not in distinct_positions:
            distinct_positions.append((next_position, direction))
        else:
            print("Found loop")
            return 1
        current_position = next_position
    return 0


def get_loops(file_name: str) -> int:
    map: List[List[str]] = process_file(
        file_name=file_name, process=lambda x: [c for c in x.replace("\n", "")]
    )
    obstacles, current_position, borders = _parse_map(map=map)
    initial_position = current_position
    possible_obstacles: List[Position] = _get_route(
        obstacles=obstacles, borders=borders, current_position=current_position
    )
    possible_obstacles.remove(initial_position)

    tasks: List[Future[int]]
    run: int = 0
    with ProcessPoolExecutor() as executor:
        tasks = [
            executor.submit(
                _task, new_obstacles, borders, initial_position, (run := run + 1)
            )
            for new_obstacles in generate_new_obstacles(
                obstacles=obstacles, possible_obstacles=possible_obstacles
            )
        ]

    return sum(task.result() for task in tasks)


def main() -> None:
    file_name: str = "input/day6/input.txt"

    part_one = get_distinct_positions(file_name=file_name)
    print("Part one solution is:", part_one)

    # Part two takes more than 20 minutes D:
    part_two = get_loops(file_name=file_name)
    print("Part two solution is:", part_two)


if __name__ == "__main__":
    main()
