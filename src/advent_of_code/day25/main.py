from itertools import filterfalse, product
from typing import Generator, List, Tuple, TypeAlias
from advent_of_code.utils.file_utils import process_file

Lock: TypeAlias = List[int]
Key: TypeAlias = List[int]


def batched(
    starting_list: List[str], batch_size: int
) -> Generator[List[str], None, None]:
    for i in range(0, len(starting_list), batch_size):
        batch = starting_list[i : i + batch_size]
        yield batch


def get_locks_and_keys(file_name: str) -> Tuple[List[Lock], List[Key]]:
    lines = process_file(
        file_name=file_name, process=lambda line: line.replace("\n", "")
    )

    def map_to_lock(batch: List[str]) -> Lock:
        return [
            max([row for row in range(len(batch)) if batch[row][column] == "#"])
            for column in range(len(batch[0]))
        ]

    def map_to_key(batch: List[str]) -> Key:
        return [
            6 - min([row for row in range(len(batch)) if batch[row][column] == "#"])
            for column in range(len(batch[0]))
        ]

    def predicate(batch: List[str]) -> bool:
        return all(batch[0][column] == "#" for column in range(len(batch[0])))

    batches = list(batched(list(filter(lambda line: line != "", lines)), batch_size=7))
    locks = list(
        map(
            map_to_lock,
            filter(predicate, batches),
        )
    )
    keys = list(
        map(
            map_to_key,
            filterfalse(predicate, batches),
        )
    )

    return locks, keys


def solve_part_one(file_name: str) -> int:
    locks, keys = get_locks_and_keys(file_name=file_name)

    def height_overlap(zips: List[Tuple[int, int]]) -> bool:
        return all(lock + key <= 5 for lock, key in zips)

    return sum(
        map(
            height_overlap,
            map(lambda item: list(zip(item[0], item[1])), product(locks, keys)),
        )
    )


def main() -> None:
    file_name = "input/day25/input.txt"

    part_one = solve_part_one(file_name=file_name)
    print("Part one solution is", part_one)


if __name__ == "__main__":
    main()
