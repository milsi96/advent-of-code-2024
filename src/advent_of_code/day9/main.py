from typing import Dict, List, Set, Tuple
from advent_of_code.utils.file_utils import process_file

dot = "."


def parse_file_system(file_name: str) -> Tuple[Dict[str, List[int]], List[str]]:
    input: List[int] = process_file(
        file_name=file_name, process=lambda x: list(map(int, x.replace("\n", "")))
    )[0]
    current_file_number: int = 0
    acc: List[str] = []
    for i in range(len(input)):
        if i % 2 == 0:
            for _ in range(input[i]):
                acc.append(str(current_file_number))
            current_file_number += 1
        else:
            for _ in range(input[i]):
                acc.append(dot)

    filesystem: Dict[str, List[int]] = {}
    for i in range(len(acc)):
        current_indexes = filesystem.get(acc[i], [])
        current_indexes.append(i)
        filesystem[acc[i]] = current_indexes

    return filesystem, list(filter(lambda ch: ch != dot, acc))


def get_checksum(filesystem: Dict[str, List[int]]) -> int:
    return sum(
        sum(int(file) * index for index in indexes)
        for file, indexes in filesystem.items()
        if file != dot
    )


def remove_empty_spaces(file_name: str) -> int:
    filesystem, non_empty_spaces = parse_file_system(file_name=file_name)

    for empty_space in sorted(filesystem[dot]):
        last_non_empty_item = non_empty_spaces.pop(-1)
        last_non_empty_space = max(filesystem[last_non_empty_item])
        if empty_space >= last_non_empty_space:
            break
        filesystem[last_non_empty_item].remove(last_non_empty_space)
        filesystem[last_non_empty_item].append(empty_space)
        filesystem[dot].remove(empty_space)

    return get_checksum(filesystem=filesystem)


def get_empty_chunks(empty_indexes: List[int]) -> List[List[int]]:
    chunk: List[int] = []
    result: List[List[int]] = []
    for i in range(len(empty_indexes) - 1):
        chunk.append(empty_indexes[i])
        if empty_indexes[i + 1] - empty_indexes[i] > 1:
            result.append(chunk)
            chunk = []
    return result


def move_files(file_name: str) -> int:
    filesystem, _ = parse_file_system(file_name=file_name)
    empty_chunks = get_empty_chunks(empty_indexes=filesystem[dot])
    already_moved: Set[str] = set()

    while True:
        empty_chunk = empty_chunks[0]
        chunk_length = len(empty_chunk)
        try:
            substitute = max(
                map(
                    lambda entry: entry[0],
                    filter(
                        lambda entry: len(entry[1]) <= chunk_length
                        and entry[0] not in already_moved,
                        filesystem.items(),
                    ),
                )
            )
        except ValueError:
            break
        updated_indexes = empty_chunk.copy()
        for i in range(len(filesystem[substitute])):
            filesystem[dot].remove(empty_chunk[i])
        filesystem[substitute] = updated_indexes[: len(filesystem[substitute])]
        already_moved.add(substitute)
        print(empty_chunk, substitute, len(filesystem[substitute]))
        empty_chunks = get_empty_chunks(empty_indexes=filesystem[dot])

    return get_checksum(filesystem=filesystem)


def main() -> None:
    file_name: str = "input/day9/input.txt"

    part_one = remove_empty_spaces(file_name=file_name)
    print("Part one solution is:", part_one)

    part_two = move_files(file_name=file_name)
    print("Part two solution is:", part_two)


if __name__ == "__main__":
    main()
