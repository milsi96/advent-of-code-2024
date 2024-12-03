import re
from typing import List

from advent_of_code.utils.file_utils import process_file

def get_result_with_donts(file_name: str) -> int:
  input: str = apply_donts(''.join(process_file(file_name=file_name, process=lambda x: x)))
  multiplications = re.findall(r"mul\(\d+,\d+\)", input)
  numbers = [result.groups() for m in multiplications if (result := re.search(r"mul\((\d+),(\d+)\)", m)) is not None]
  return sum(map(lambda t: int(t[0]) * int(t[1]), numbers))
  return 0

def get_multiplications_result(file_name: str) -> int:
  input: List[str] = process_file(file_name=file_name, process=lambda x: x)
  multiplications = re.findall(r"mul\(\d+,\d+\)", ''.join(input))
  numbers = [result.groups() for m in multiplications if (result := re.search(r"mul\((\d+),(\d+)\)", m)) is not None]
  return sum(map(lambda t: int(t[0]) * int(t[1]), numbers))

def apply_donts(line: str) -> str:
  return re.sub(r"don't\(\).*?do\(\)", "", line.replace("\n", ""))

def main() -> None:
  file_name: str = "input/day3/input.txt"

  first_part = get_multiplications_result(file_name=file_name)
  print("Part one solution is", first_part)

  second_part = get_result_with_donts(file_name=file_name)
  print("Part one solution is", second_part)


if __name__ == "__main__":
  main()