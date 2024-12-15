from enum import StrEnum
from typing import Dict, List, Set, Tuple, TypeAlias
from advent_of_code.utils.file_utils import process_file

Coordinate: TypeAlias = Tuple[int, int]
Direction: TypeAlias = Tuple[int, int]

X = 0
Y = 1

GPS_FACTOR = 100
RESIZE_FACTOR = 2


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


def get_resized_items(
    items: Dict[Coordinate, Item],
) -> Tuple[Dict[Coordinate, Item], Dict[Coordinate, Coordinate]]:
    new_items: Dict[Coordinate, Item] = dict()
    boxes: Dict[Coordinate, Coordinate] = dict()

    for coord, item in items.items():
        new_items[(first := (coord[X], coord[Y] * RESIZE_FACTOR))] = item
        if item is not Item.ROBOT:
            new_items[(second := (coord[X], coord[Y] * RESIZE_FACTOR + 1))] = item
        if item is Item.BOX:
            boxes[first] = second
            boxes[second] = first

    return new_items, boxes


def get_robot(items: Dict[Coordinate, Item]) -> Coordinate:
    for coordinate, item in items.items():
        if item == Item.ROBOT:
            return coordinate
    raise ValueError("Robot was not found")


def apply_move(
    item_stack: List[Coordinate], items: Dict[Coordinate, Item], move: Move
) -> List[Coordinate]:
    direction = move.get_direction()

    if all(
        (next_coord := (item[X] + direction[X], item[Y] + direction[Y]))
        not in items.keys()
        or items[next_coord] is not Item.WALL
        for item in item_stack
    ):
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


def print_warehouse(items: Dict[Coordinate, Item], resized: bool = False) -> None:
    height = max(map(lambda coord: coord[X], items.keys())) + 1
    width = height if not resized else height * 2

    for row in range(height):
        line = ""
        for column in range(width):
            line += (
                "." if (row, column) not in items.keys() else items[(row, column)].value
            )
        print(line)


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


def solve_part_two(file_name: str) -> int:
    base_items, moves = get_input(file_name=file_name)
    items, boxes = get_resized_items(items=base_items)

    for move in moves:
        stack = get_stack(robot=get_robot(items=items), items=items, move=move)

        while True:
            matching_boxes = [boxes[s] for s in stack if s in boxes]
            if all(match in stack for match in matching_boxes):
                break
            for match in matching_boxes:
                if match not in stack:
                    stack.extend(get_stack(robot=match, items=items, move=move))

        updated_coordinates = apply_move(item_stack=stack, items=items, move=move)

        if len(set(updated_coordinates) - set(stack)) != 0:
            direction = move.get_direction()
            moved_boxes = {
                (box[X] + direction[X], box[Y] + direction[Y]): (
                    match[X] + direction[X],
                    match[Y] + direction[Y],
                )
                for box, match in boxes.items()
                if box in stack
            }
            _ = [boxes.pop(box) for box in stack if items[box] is Item.BOX]
            for box, match in moved_boxes.items():
                boxes[box] = match

        stack_items = [items.pop(i) for i in stack]
        for item, new_coord in zip(stack_items, updated_coordinates):
            items[new_coord] = item

        # uncomment this sleep to see the robot move boxes
        # print_warehouse(items=items, resized=True)
        # print()
        # time.sleep(0.3)

    return get_resized_gps_coordinates(boxes=boxes)


def get_resized_gps_coordinates(boxes: Dict[Coordinate, Coordinate]) -> int:
    target_boxes: Set[Coordinate] = set()
    for box, match in boxes.items():
        target_boxes.add(min([box, match], key=lambda b: b[Y]))

    return sum(map(get_gps_coordinate, target_boxes))


def main() -> None:
    file_name: str = "input/day15/input.txt"

    part_one = solve_part_one(file_name=file_name)
    print("Part one solution is", part_one)

    part_two = solve_part_two(file_name=file_name)
    print("Part two solution is:", part_two)


if __name__ == "__main__":
    main()
