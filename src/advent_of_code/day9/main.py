from typing import Dict, List
from advent_of_code.utils.file_utils import process_file

dot = -1


def parse_file_system(file_name: str) -> Dict[int, List[int]]:
    input: list[int] = process_file(
        file_name=file_name, process=lambda x: list(map(int, x.replace("\n", "")))
    )[0]
    current_file_number: int = 0
    current_index: int = -1
    filesystem: dict[int, list[int]] = {}

    for i in range(len(input)):
        new_indexes = [(current_index := current_index + 1) for _ in range(input[i])]
        if i % 2 == 0:
            filesystem[current_file_number] = new_indexes
            current_file_number += 1
        else:
            free_space = filesystem.get(dot, [])
            free_space.extend(new_indexes)
            filesystem[dot] = free_space

    return filesystem


def get_checksum(filesystem: Dict[int, List[int]]) -> int:
    return sum(
        sum(file * index for index in indexes)
        for file, indexes in filesystem.items()
        if file != dot
    )


def get_non_empty_spaces(filesystem: Dict[int, List[int]]) -> List[int]:
    return [
        index
        for file in [
            [key for _ in range(len(value))]
            for key, value in sorted(filesystem.items())
            if key != dot
        ]
        for index in file
    ]


def fill_empty_spaces(file_name: str) -> int:
    filesystem = parse_file_system(file_name=file_name)
    non_empty_spaces = get_non_empty_spaces(filesystem=filesystem)

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
    filesystem = parse_file_system(file_name=file_name)
    empty_chunks = get_empty_chunks(empty_indexes=filesystem[dot])

    for file in sorted(filesystem.keys(), reverse=True):
        if file == dot:
            continue

        print(file)
        file_length = len(filesystem[file])

        def find_empty_chunk(empty_spaces: List[int], file_len: int) -> List[int]:
            result: List[int] = [empty_spaces[0]]
            for empty_space in empty_spaces[1:]:
                if result[-1] - empty_space and len(result) < file_len:
                    result.clear()
                    continue
                result.append(empty_space)

            return result

        if (
            empty_chunk_index := find_empty_chunk(
                empty_spaces=filesystem[dot], file_len=file_length
            )
        ) == []:
            print("File", file, "couldn't be moved")
            continue

        filesystem[file].clear()
        filesystem[file].extend(
            (empty_chunk := empty_chunks[empty_chunk_index])[:file_length]
        )
        del empty_chunks[empty_chunk_index]
        if (to_append := empty_chunk[file_length:]) != []:
            empty_chunks.append(to_append)
        empty_chunks = get_empty_chunks(
            empty_indexes=sorted([index for chunk in empty_chunks for index in chunk])
        )
        empty_chunks.sort(key=lambda chunk: chunk[0])

    return get_checksum(filesystem=filesystem)


def main() -> None:
    file_name: str = "input/day9/input.txt"

    part_one = fill_empty_spaces(file_name=file_name)
    print("Part one solution is:", part_one)

    part_two = move_files(file_name=file_name)
    print("Part two solution is:", part_two)
    # 6636608781232


if __name__ == "__main__":
    main()
