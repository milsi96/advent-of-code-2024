from typing import Dict, List
from advent_of_code.utils.file_utils import process_file


def get_checksum(file_name: str) -> int:
  input: List[int] = process_file(file_name=file_name, process=lambda x: list(map(int, x.replace("\n", ""))))[0]
  current_file_number: int = 0
  dot = "."
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

  non_empty_spaces = list(filter(lambda ch: ch != dot, acc))
  for empty_space in sorted(filesystem[dot]):
    last_non_empty_item = non_empty_spaces.pop(-1)
    last_non_empty_space = max(filesystem[last_non_empty_item])
    if empty_space >= last_non_empty_space:
      break
    filesystem[last_non_empty_item].remove(last_non_empty_space)
    filesystem[last_non_empty_item].append(empty_space)
    filesystem[dot].remove(empty_space)

  return sum(sum(int(file) * index for index in indexes) for file, indexes in filesystem.items() if file != dot)

def main() -> None:
  file_name: str = "input/day9/input.txt"

  part_one = get_checksum(file_name=file_name)
  print("Part one solution is:", part_one)


if __name__ == "__main__":
  main()