from typing import Generator, List, Tuple

from advent_of_code.utils.file_utils import process_file
from advent_of_code.day18.main import Point, dijkstra
from advent_of_code.day12.main import get_manhattan_distance


def get_track(file_name: str) -> Tuple[List[Point], List[Point], Point, Point]:
    lines: List[str] = process_file(
        file_name=file_name, process=lambda line: line.replace("\n", "")
    )
    points: List[Point] = list()
    walls: List[Point] = list()
    start: Point
    end: Point

    for row in range(len(lines)):
        for column in range(len(lines[row])):
            if (value := lines[row][column]) == "#":
                walls.append((row, column))
                continue

            points.append((row, column))
            if value == "S":
                walls.append((row, column))
                start = (row, column)
            elif value == "E":
                walls.append((row, column))
                end = (row, column)

    return points, walls, start, end


def get_cheats_for_track(
    original_track: List[Point],
) -> Generator[Tuple[Point, Point], None, None]:
    def get_end_of_cheat(
        track: List[Point], target: Point
    ) -> Generator[Point, None, None]:
        for point in track:
            if get_manhattan_distance(target, point) != 2:
                continue
            if point not in track:
                continue
            yield point
        return None

    for i in range(len(original_track)):
        cheat_start = original_track[i]
        for cheat_end in get_end_of_cheat(track=original_track[i:], target=cheat_start):
            if cheat_end is not None:
                yield cheat_start, cheat_end


def solve_part_one(file_name: str, picoseconds_limit: int = 0) -> int:
    points, _, start, end = get_track(file_name=file_name)
    distances, path = dijkstra(maze=list(points), start=start, end=end)
    result = 0

    for cheat_start, cheat_end in get_cheats_for_track(original_track=path):
        saved_picoseconds = distances[cheat_end] - (distances[cheat_start] + 2)
        if saved_picoseconds != 0 and saved_picoseconds >= picoseconds_limit:
            result += 1

    return result


def solve_part_two(file_name: str, picoseconds_limit: int = 0) -> int:
    return 0


def main() -> None:
    file_name = "input/day20/input.txt"

    part_one = solve_part_one(file_name=file_name, picoseconds_limit=100)
    print("Part one solution is", part_one)


if __name__ == "__main__":
    main()
