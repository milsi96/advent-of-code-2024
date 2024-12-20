from typing import Generator, List, Tuple

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
    original_track: List[Point], max_distance: int, picoseconds_limit: int
) -> Generator[Tuple[Point, Point], None, None]:
    def get_end_of_cheat(
        track: List[Point], target: Point
    ) -> Generator[Point, None, None]:
        for point in track:
            if get_manhattan_distance(target, point) > max_distance:
                continue
            if point not in track:
                continue
            yield point
        return None

    if picoseconds_limit > len(original_track):
        return None

    for i in range(len(original_track)):
        cheat_start = original_track[i]
        for cheat_end in get_end_of_cheat(
            track=original_track[i + picoseconds_limit :], target=cheat_start
        ):
            if cheat_end is not None:
                yield cheat_start, cheat_end


def get_total_cheats(
    file_name: str, max_distance: int, picoseconds_limit: int = 0
) -> int:
    points, start, end = get_track(file_name=file_name)
    distances, path = dijkstra(maze=list(points), start=start, end=end)
    result = 0

    for cheat_start, cheat_end in get_cheats_for_track(
        original_track=path,
        max_distance=max_distance,
        picoseconds_limit=picoseconds_limit,
    ):
        saved_picoseconds = distances[cheat_end] - (
            distances[cheat_start] + get_manhattan_distance(cheat_start, cheat_end)
        )
        if saved_picoseconds != 0 and saved_picoseconds >= picoseconds_limit:
            result += 1

    return result


def main() -> None:
    file_name = "input/day20/input.txt"

    part_one = get_total_cheats(
        file_name=file_name, picoseconds_limit=100, max_distance=2
    )
    print("Part one solution is", part_one)

    part_two = get_total_cheats(
        file_name=file_name, picoseconds_limit=100, max_distance=20
    )
    print("Part two solution is", part_two)


if __name__ == "__main__":
    main()
