from collections import defaultdict
from itertools import product
from typing import DefaultDict, Dict, List, Tuple, TypeAlias
from advent_of_code.utils.file_utils import process_file


Square: TypeAlias = Tuple[int, int]
ROW: int = 0
COLUMN: int = 1


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
        perimeter += 4 - adjacent_squares

    return perimeter


def get_area(squares: List[Square]) -> int:
    return len(squares)


def get_total_price(file_name: str) -> int:
    return sum(
        get_perimeter(squares=sub_region) * get_area(squares=sub_region)
        for _, squares in get_regions(file_name=file_name).items()
        for sub_region in groupby_adjacent_regions(squares=squares)
    )


def main() -> None:
    file_name: str = "input/day12/input.txt"

    part_one = get_total_price(file_name=file_name)
    print("Part one solution is", part_one)


if __name__ == "__main__":
    main()
