from collections import defaultdict
from functools import partial
from typing import DefaultDict, Dict, Generator
from itertools import groupby

from advent_of_code.utils.file_utils import process_file


def get_input(file_name: str) -> DefaultDict[int, int]:
    def _process_stones(line: str) -> DefaultDict[int, int]:
        return defaultdict(
            int,
            {
                int(number): len(list(occurrence))
                for number, occurrence in groupby(
                    [int(number) for number in line.replace("\n", "").split(" ")]
                )
            },
        )

    return process_file(file_name=file_name, process=_process_stones)[0]


def get_total_stones(stones: Dict[int, int]) -> int:
    return sum([value for _, value in stones.items()])


def execute_cycles(file_name: str, cycles: int) -> int:
    stones: DefaultDict[int, int] = get_input(file_name=file_name)
    for _ in range(cycles):
        updated_stones: Dict[int, int] = defaultdict(int)
        for stone_value in [stone for stone, amount in stones.items() if amount != 0]:
            for new_stone_value in blink(stone_value=stone_value):
                updated_stones[new_stone_value] += stones[stone_value]
            stones[stone_value] -= stones[stone_value]
        for key, value in updated_stones.items():
            stones[key] += value
    return get_total_stones(stones=stones)


def blink(stone_value: int) -> Generator[int, None, None]:
    if stone_value == 0:
        yield 1
    elif (stone_length := len((stone_string := str(stone_value)))) % 2 == 0:
        half = int(stone_length / 2)
        first_half, second_half = stone_string[:half], stone_string[half:]
        yield int(first_half)
        yield int(second_half)
    else:
        yield stone_value * 2024


def main() -> None:
    file_name: str = "input/day11/input.txt"

    execute_cycles_partial = partial(execute_cycles, file_name)

    part_one, part_two = tuple(
        map(lambda cycles: execute_cycles_partial(cycles), [25, 75])
    )
    print("Part one solution is", part_one)
    print("Part two solution is", part_two)


if __name__ == "__main__":
    main()
