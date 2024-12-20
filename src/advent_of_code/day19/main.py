from datetime import datetime, timedelta
from functools import partial
from typing import List, Set, Tuple, TypeAlias

from cachetools import TTLCache, cached  # type: ignore

from advent_of_code.utils.file_utils import process_file

Design: TypeAlias = str
Pattern: TypeAlias = str


def get_input(file_name: str) -> Tuple[List[Design], List[Pattern]]:
    lines = process_file(
        file_name=file_name, process=lambda line: line.replace("\n", "")
    )
    patterns: List[Pattern]
    designs: List[Design] = list()

    for line in lines:
        if "," in line:
            patterns = line.split(", ")
        elif len(line) == 0:
            continue
        else:
            designs.append(line)

    return designs, patterns


def key(patterns: Set[Pattern], design: Design) -> str:
    return design


@cached(
    cache=TTLCache(maxsize=10000, ttl=timedelta(hours=12), timer=datetime.now), key=key
)
def get_arrangements(patterns: Set[Pattern], design: Design) -> int:
    if design == "":
        return 1

    arrangements = 0
    for i in range(1, len(design) + 1):
        if (
            design[:i] in patterns
            and (
                new_arrangements := get_arrangements(
                    patterns=patterns, design=design[i:]
                )
            )
            > 0
        ):
            arrangements += new_arrangements

    return arrangements


def solve_part_one(file_name: str) -> int:
    designs, patterns = get_input(file_name=file_name)
    return len(list(filter(partial(get_arrangements, set(patterns)), designs)))


def solve_part_two(file_name: str) -> int:
    designs, patterns = get_input(file_name=file_name)
    return sum(map(partial(get_arrangements, set(patterns)), designs))


def main() -> None:
    file_name = "input/day19/input.txt"

    part_one = solve_part_one(file_name=file_name)
    print("Part one solution is", part_one)

    part_two = solve_part_two(file_name=file_name)
    print("Part two solution is", part_two)


if __name__ == "__main__":
    main()
