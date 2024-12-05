from dataclasses import dataclass
from functools import partial
from typing import List
from advent_of_code.utils.file_utils import process_file

@dataclass
class Rule:
  before: int
  after: int


def get_middle_page_sum(file_name: str) -> int:
  input: List[str] = process_file(file_name=file_name, process=lambda x: x)
  
  def _process_rule(line: str) -> Rule:
    numbers = line.split("|")
    return Rule(before=int(numbers[0]), after=int(numbers[1]))
  
  def _process_update(line: str) -> List[int]:
    return list(map(lambda update: int(update), line.split(",")))

  rules: List[Rule] = list(map(_process_rule, filter(lambda line: "|" in line, input)))
  updates: List[List[int]] = list(map(_process_update, filter(lambda line: "," in line, input)))
  valid_updates: List[List[int]] = list(filter(partial(_is_update_valid, rules), updates))
  return sum(map(lambda update: update[int(len(update)/2)], valid_updates))


def _is_update_valid(rules: List[Rule], update: List[int]) -> bool:
  for i in range(len(update)):
    applicable_rules = list(filter(lambda rule: rule.after == update[i], rules))
    before_numbers: List[int] = list(map(lambda rule: rule.before, applicable_rules))
    if any(num in update[i+1:] for num in before_numbers):
      return False
  return True



def main() -> None:
  file_name: str = "input/day5/input.txt"

  part_one = get_middle_page_sum(file_name=file_name)
  print("Part one solution is:", part_one)


if __name__ == "__main__":
  main()