from collections import defaultdict
from itertools import groupby, product
from typing import Callable, DefaultDict, Dict, List, Tuple, TypeAlias

from shapely import Point, Polygon, unary_union
from advent_of_code.utils.file_utils import process_file


Square: TypeAlias = Tuple[int, int]
ROW: int = 0
COLUMN: int = 1
SIDES: int = 4


def get_regions(file_name: str) -> DefaultDict[str, List[Square]]:
    input: List[str] = process_file(
        file_name=file_name, process=lambda line: line.replace("\n", "")
    )
    result: DefaultDict[str, List[Square]] = defaultdict(list)

    for row in range(len(input)):
        for column in range(len(input[row])):
            result[input[row][column]].append((row, column))

    return result


def get_adjacent_squares(square: Square) -> List[Square]:
    return [
        (square[ROW] + drow, square[COLUMN] + dcolumn)
        for drow, dcolumn in [(0, 1), (0, -1), (1, 0), (-1, 0)]
    ]


def get_manhattan_distance(square1: Square, square2: Square):
    return abs(square1[0] - square2[0]) + abs(square1[1] - square2[1])


def groupby_adjacent_regions(squares: List[Square]) -> List[List[Square]]:
    parent = {square: square for square in squares}

    def find(square):
        if parent[square] != square:
            parent[square] = find(parent[square])
        return parent[square]

    def union(square1, square2):
        root1 = find(square1)
        root2 = find(square2)
        if root1 != root2:
            parent[root2] = root1

    for square1, square2 in product(squares, repeat=2):
        if get_manhattan_distance(square1, square2) == 1:
            union(square1, square2)

    groups: Dict[Square, List[Square]] = {}
    for square in squares:
        root = find(square)
        if root not in groups:
            groups[root] = []
        groups[root].append(square)

    return list(groups.values())


def get_perimeter(squares: List[Square]) -> int:
    perimeter: int = 0
    for square in squares:
        adjacent_squares = sum(
            adj_square in squares for adj_square in get_adjacent_squares(square=square)
        )
        perimeter += SIDES - adjacent_squares

    return perimeter


def count_edges(coordinates: List[Tuple[float, float]]):
    def direction(p1, p2):
        return (p2[0] - p1[0], p2[1] - p1[1])

    if len(coordinates) < 3:
        return 0

    directions = [
        direction(coordinates[i - 1], coordinates[i])
        for i in range(1, len(coordinates))
    ]
    edges = len((unique_directions := [dir[0] for dir in groupby(directions)]))

    if unique_directions[0] == unique_directions[-1]:
        # it may happen that coordinates don't start from an edge
        edges -= 1

    return edges


def get_sides(squares: List[Square]) -> int:
    polygons = [
        Polygon(list(point.buffer(0.5, cap_style="square").exterior.coords))
        for point in list(map(Point, squares))
    ]
    merged_polygon = unary_union(polygons)
    return count_edges(
        [coord for coord in list(iter(merged_polygon.exterior.coords))]  # type: ignore
    ) + sum(
        [
            count_edges(list(iter(interior.coords)))
            for interior in merged_polygon.interiors  # type: ignore
        ]
    )


def get_area(squares: List[Square]) -> int:
    return len(squares)


def get_total_price(
    regions: Dict[str, List[Square]],
    first_value_getter: Callable[[List[Square]], int],
    second_value_getter: Callable[[List[Square]], int],
) -> int:
    return sum(
        first_value_getter(sub_region) * second_value_getter(sub_region)
        for _, squares in regions.items()
        for sub_region in groupby_adjacent_regions(squares=squares)
    )


def solve_part_one(file_name: str) -> int:
    return get_total_price(get_regions(file_name=file_name), get_perimeter, get_area)


def solve_part_two(file_name: str) -> int:
    return get_total_price(get_regions(file_name=file_name), get_area, get_sides)


def main() -> None:
    file_name: str = "input/day12/input.txt"

    part_one = solve_part_one(file_name=file_name)
    print("Part one solution is", part_one)

    part_two = solve_part_two(file_name=file_name)
    print("Part two solution is", part_two)


if __name__ == "__main__":
    main()
