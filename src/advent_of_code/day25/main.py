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

    def predicate(batch: List[str]) -> bool:
        return all(batch[0][column] == "#" for column in range(len(batch[0])))

    batches = list(batched(list(filter(lambda line: line != "", lines)), batch_size=7))
    locks = list(
        map(
            lambda batch: [
                max([row for row in range(len(batch)) if batch[row][column] == "#"])
                for column in range(len(batch[0]))
            ],
            filter(predicate, batches),
        )
    )
    keys = list(
        map(
            lambda batch: [
                6 - min([row for row in range(len(batch)) if batch[row][column] == "#"])
                for column in range(len(batch[0]))
            ],
            filterfalse(predicate, batches),
        )
    )

    return locks, keys


def solve_part_one(file_name: str) -> int:
    locks, keys = get_locks_and_keys(file_name=file_name)
    return sum(
        list(
            map(
                lambda zips: all(n_lock + n_key <= 5 for n_lock, n_key in zips),
                map(lambda item: zip(item[0], item[1]), product(locks, keys)),
            )
        )
    )


def main() -> None:
    file_name = "input/day25/input.txt"

    part_one = solve_part_one(file_name=file_name)
    print("Part one solution is", part_one)


if __name__ == "__main__":
    main()
