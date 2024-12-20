from typing import Generator, List, Tuple

from advent_of_code.day16.main import COLUMN, ROW
from advent_of_code.utils.file_utils import process_file
from advent_of_code.day18.main import Point, dijkstra
from advent_of_code.day12.main import get_manhattan_distance


def get_track(file_name: str) -> Tuple[List[Point], Point, Point]:
    lines: List[str] = process_file(
        file_name=file_name, process=lambda line: line.replace("\n", "")
    )
    points: List[Point] = list()
    start: Point
    end: Point

    for row in range(len(lines)):
        for column in range(len(lines[row])):
            if (value := lines[row][column]) == "#":
                continue

            points.append((row, column))
            if value == "S":
                start = (row, column)
            elif value == "E":
                end = (row, column)

    return points, start, end


def get_cheats_for_track(
    original_track: List[Point], max_cheat_time: int
) -> Generator[Tuple[Point, Point, Point], None, None]:
    def get_mid_point(p1: Point, p2: Point) -> Point:
        return (
            (p1[ROW] + p2[ROW]) // max_cheat_time,
            (p1[COLUMN] + p2[COLUMN]) // max_cheat_time,
        )

    def get_end_cheat(
        track: List[Point], target: Point
    ) -> Generator[Tuple[Point, Point], None, None]:
        for point in track:
            if get_manhattan_distance(target, point) != max_cheat_time:
                continue
            if (wall := get_mid_point(target, point)) in track:
                continue
            if point not in track:
                continue
            yield point, wall

        return None

    for point in original_track:
        for end_cheat, wall in get_end_cheat(track=original_track, target=point):
            if (end_cheat, wall) is not None:
                yield point, wall, end_cheat


def solve_part_one(
    file_name: str, max_cheat_time: int = 2, picoseconds_limit: int = 0
) -> int:
    points, start, end = get_track(file_name=file_name)
    distances, path = dijkstra(maze=list(points), start=start, end=end)
    result = 0

    for start_cheat, _, end_cheat in get_cheats_for_track(
        original_track=path, max_cheat_time=max_cheat_time
    ):
        saved_picoseconds = distances[end_cheat] - (
            distances[start_cheat] + max_cheat_time
        )
        if saved_picoseconds != 0 and saved_picoseconds >= picoseconds_limit:
            result += 1

    return result


def main() -> None:
    file_name = "input/day20/input.txt"

    part_one = solve_part_one(file_name=file_name, picoseconds_limit=100)
    print("Part one solution is", part_one)


if __name__ == "__main__":
    main()
