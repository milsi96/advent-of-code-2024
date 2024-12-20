from functools import partial
from itertools import dropwhile
from typing import Dict, Generator, List, Tuple

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
    base_track: List[Point], max_distance: int, picoseconds_limit: int
) -> Generator[Tuple[Point, Point], None, None]:
    def get_cheat_ends(track: List[Point], target: Point) -> List[Point]:
        manhattan_distance = partial(get_manhattan_distance, target)
        return [point for point in track if manhattan_distance(point) <= max_distance]

    def get_points_at_distance(
        track: List[Point], current_index: int, limit: int
    ) -> List[Point]:
        track_with_index = enumerate(track)
        return list(
            map(
                lambda entry: entry[1],
                dropwhile(lambda el: el[0] < current_index + limit, track_with_index),
            )
        )

    track_with_index = enumerate(base_track)
    for index, point in track_with_index:
        for end in get_cheat_ends(
            track=get_points_at_distance(base_track, index, picoseconds_limit),
            target=point,
        ):
            yield point, end


def get_total_cheats(
    file_name: str, max_distance: int, picoseconds_limit: int = 0
) -> int:
    points, start, end = get_track(file_name=file_name)
    distances, path = dijkstra(maze=list(points), start=start, end=end)

    def get_saved_picoseconds(
        distances: Dict[Point, int], cheat_start: Point, cheat_end: Point
    ) -> int:
        return distances[cheat_end] - (
            distances[cheat_start] + get_manhattan_distance(cheat_start, cheat_end)
        )

    def is_cheat_valid(
        distances: Dict[Point, int], picoseconds_limit: int, cheat: Tuple[Point, Point]
    ) -> bool:
        cheat_start, cheat_end = cheat
        saved_picoseconds = partial(
            get_saved_picoseconds, distances, cheat_start, cheat_end
        )
        return True if max(0, picoseconds_limit - 1) < saved_picoseconds() else False

    return sum(
        map(
            partial(is_cheat_valid, distances, picoseconds_limit),
            list(
                get_cheats_for_track(
                    base_track=path,
                    max_distance=max_distance,
                    picoseconds_limit=picoseconds_limit,
                )
            ),
        )
    )


def main() -> None:
    file_name = "input/day20/input.txt"
    limit = 100
    distance = 2

    part_one = get_total_cheats(
        file_name=file_name, picoseconds_limit=limit, max_distance=distance
    )
    print("Part one solution is", part_one)

    part_two = get_total_cheats(
        file_name=file_name, picoseconds_limit=limit, max_distance=distance * 10
    )
    print("Part two solution is", part_two)


if __name__ == "__main__":
    main()
