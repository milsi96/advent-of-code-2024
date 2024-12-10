from typing import Callable, List, Tuple

from advent_of_code.utils.file_utils import process_file


def _get_input(
    file_name: str, process: Callable[[str], Tuple[int, int]]
) -> Tuple[List[int], List[int]]:
    result = process_file(file_name=file_name, process=process)
    list1, list2 = [row[0] for row in result], [row[1] for row in result]
    assert len(list1) == len(list2)
    return (list1, list2)


def get_distances(file_name: str) -> int:
    list1, list2 = _get_input(file_name=file_name, process=_parse_into_numbers)
    list1.sort()
    list2.sort()

    return sum([abs(list1[i] - list2[i]) for i in range(len(list1))])


def _parse_into_numbers(line: str) -> Tuple[int, int]:
    numbers = [int(n) for n in line.split("   ")]
    assert len(numbers) == 2
    return (numbers[0], numbers[1])


def get_similarity(file_name: str) -> int:
    list1, list2 = _get_input(file_name=file_name, process=_parse_into_numbers)
    return sum([n * list2.count(n) for n in list1 if n in list2])


def main() -> None:
    file_name: str = "input/day1/input.txt"

    distances = get_distances(file_name=file_name)
    print("Part one result is", distances)

    similarity = get_similarity(file_name=file_name)
    print("Part two result is", similarity)


if __name__ == "__main__":
    main()
