from typing import Dict, List, Tuple
from advent_of_code.utils.file_utils import process_file
from itertools import repeat

empty = -1


def parse_file_system(file_name: str) -> List[int]:
    input: list[int] = process_file(
        file_name=file_name, process=lambda x: list(map(int, x.replace("\n", "")))
    )[0]
    current_file_number: int = -1
    filesystem: List[int] = []

    for i in range(len(input)):
        if i % 2 == 0:
            filesystem.extend(
                list(repeat((current_file_number := current_file_number + 1), input[i]))
            )
        else:
            filesystem.extend(list(repeat(empty, input[i])))

    return filesystem


def compact_parse(file_name: str) -> Tuple[List[int], Dict[int, int]]:
    input: list[int] = process_file(
        file_name=file_name, process=lambda x: list(map(int, x.replace("\n", "")))
    )[0]

    current_file_number: int = -1
    filesystem: List[int] = []
    file_lengths: Dict[int, int] = dict()

    for i in range(len(input)):
        if i % 2 == 0:
            filesystem.append((current_file_number := current_file_number + 1))
            file_lengths[current_file_number] = input[i]
        else:
            if input[i] != 0:
                filesystem.append(empty * input[i])

    return filesystem, file_lengths


def print_filesystem(filesystem: List[int]) -> None:
    print("".join(list(map(str, filesystem))).replace("-1", "."))


def print_compact_filesystem(
    filesystem: List[int], file_lengths: Dict[int, int]
) -> None:
    acc: str = ""
    for file in filesystem:
        if file < 0:
            acc += "." * abs(file)
        else:
            acc += str(file) * file_lengths[file]
    print(acc)


def get_checksum_compact(filesystem: List[int], file_lengths: Dict[int, int]) -> int:
    result = 0
    current_index = -1
    for file in filesystem:
        if file >= 0:
            result += sum(
                (current_index := current_index + 1) * file
                for _ in range(file_lengths[file])
            )
        else:
            current_index += abs(file)
    return result


def get_checksum(filesystem: List[int]) -> int:
    return sum(
        i * filesystem[i] for i in range(len(filesystem)) if filesystem[i] is not empty
    )


def fill_empty_spaces(file_name: str) -> int:
    filesystem: List[int] = parse_file_system(file_name=file_name)
    non_empty_filesystem = [file for file in filesystem if file is not empty]

    for file in filesystem:
        if file is not empty:
            continue
        first_empty_index = filesystem.index(empty)
        last_non_empty_index = (
            len(filesystem) - 1 - filesystem[::-1].index(non_empty_filesystem.pop(-1))
        )

        if last_non_empty_index <= first_empty_index:
            break

        filesystem[first_empty_index], filesystem[last_non_empty_index] = (
            filesystem[last_non_empty_index],
            filesystem[first_empty_index],
        )

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
    filesystem, file_lengths = compact_parse(file_name=file_name)

    for file, file_length in sorted(file_lengths.items(), reverse=True):
        empty_chunks = [
            {"index": index, "dimension": empty_chunk_dimension}
            for index, empty_chunk_dimension in enumerate(filesystem)
            if empty_chunk_dimension < 0
        ]
        next_spots = sorted(
            filter(lambda chunk: abs(chunk["dimension"]) >= file_length, empty_chunks),
            key=lambda chunk: chunk["index"],
        )
        print(file)
        if len(next_spots) == 0:
            continue
        free_spot = next_spots[0]
        free_spot_index, free_spot_dimension = (
            free_spot["index"],
            free_spot["dimension"],
        )
        if free_spot_index > filesystem.index(file):
            continue
        file_index = filesystem.index(file)

        if free_spot_dimension + file_length == 0:
            filesystem[free_spot_index], filesystem[file_index] = (
                filesystem[file_index],
                filesystem[free_spot_index],
            )
        else:
            filesystem[free_spot_index] = free_spot_dimension + file_length
            filesystem[file_index] = -file_length
            filesystem.insert(free_spot_index, file)

    return get_checksum_compact(filesystem=filesystem, file_lengths=file_lengths)


def main() -> None:
    file_name: str = "input/day9/input.txt"

    # part_one = fill_empty_spaces(file_name=file_name)
    # print("Part one solution is:", part_one)

    part_two = move_files(file_name=file_name)
    print("Part two solution is:", part_two)
    # 6636608781232


if __name__ == "__main__":
    main()
