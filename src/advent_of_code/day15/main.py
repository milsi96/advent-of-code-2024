from enum import StrEnum
from typing import Dict, List, Tuple, TypeAlias
from advent_of_code.utils.file_utils import process_file

Coordinate: TypeAlias = Tuple[int, int]
Direction: TypeAlias = Tuple[int, int]

X = 0
Y = 1

GPS_FACTOR = 100


class Item(StrEnum):
    WALL = "#"
    BOX = "O"
    ROBOT = "@"


class Move(StrEnum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

    def get_direction(self) -> Direction:
        match self:
            case Move.UP:
                return (-1, 0)
            case Move.DOWN:
                return (1, 0)
            case Move.LEFT:
                return (0, -1)
            case Move.RIGHT:
                return (0, 1)
            case _:
                raise ValueError(f"Move is not supported {self}")


def get_input(file_name: str) -> Tuple[Dict[Coordinate, Item], List[Move]]:
    lines = process_file(
        file_name=file_name, process=lambda line: line.replace("\n", "")
    )
    items: Dict[Coordinate, Item] = dict()
    moves: List[Move] = list()

    for row in range(len(lines)):
        if "#" in lines[row]:
            for column in range(len(lines[row])):
                if (symbol := lines[row][column]) == ".":
                    continue
                items[(row, column)] = Item(symbol)
        elif any(move in lines[row] for move in ["^", "v", ">", "<"]):
            moves.extend(list(map(Move, lines[row])))

    return items, moves


def get_robot(items: Dict[Coordinate, Item]) -> Coordinate:
    for coordinate, item in items.items():
        if item == Item.ROBOT:
            return coordinate
    raise ValueError("Robot was not found")


def apply_move(
    item_stack: List[Coordinate], items: Dict[Coordinate, Item], move: Move
) -> List[Coordinate]:
    last_item = item_stack[-1]
    direction = move.get_direction()

    if (
        next_coord := (last_item[X] + direction[X], last_item[Y] + direction[Y])
    ) not in items.keys() and next_coord is not Item.WALL:
        return list(
            map(lambda c: (c[X] + direction[X], c[Y] + direction[Y]), item_stack)
        )
    else:
        return item_stack


def get_stack(
    robot: Coordinate, items: Dict[Coordinate, Item], move: Move
) -> List[Coordinate]:
    result: List[Coordinate] = []
    current: Coordinate = robot
    direction: Direction = move.get_direction()

    while current in items.keys() and items[current] is not Item.WALL:
        result.append(current)
        current = (current[X] + direction[X], current[Y] + direction[Y])

    return result


def get_gps_coordinate(coordinate: Coordinate) -> int:
    return GPS_FACTOR * coordinate[X] + coordinate[Y]


def solve_part_one(file_name: str) -> int:
    items, moves = get_input(file_name=file_name)

    for move in moves:
        stack = get_stack(robot=get_robot(items=items), items=items, move=move)
        updated_coordinates = apply_move(item_stack=stack, items=items, move=move)
        stack_items = [items.pop(i) for i in stack]
        for item, new_coord in zip(stack_items, updated_coordinates):
            items[new_coord] = item

    return sum(
        map(
            get_gps_coordinate,
            [coord for coord, item in items.items() if item == Item.BOX],
        )
    )


def main() -> None:
    file_name: str = "input/day15/input.txt"

    part_one = solve_part_one(file_name=file_name)
    print("Part one solution is", part_one)

    # part_two = solve_part_two(file_name=file_name, width=101, height=103)
    # print("Part two solution is:", part_two)


if __name__ == "__main__":
    main()
