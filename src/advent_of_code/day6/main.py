
from dataclasses import dataclass
from enum import StrEnum
from typing import List, Tuple
from advent_of_code.utils.file_utils import process_file


class Direction(StrEnum):
  UP = "up"
  DOWN = "down"
  RIGHT = "right"
  LEFT = "left"

@dataclass
class Position:
  row: int
  column: int


def _get_route(obstacles: List[Position], current_position: Position, map_size: int) -> List[Position]:
  def _move(obstacles: List[Position], current_position: Position, direction: Direction) -> Tuple[Position, Direction]:
    match direction: 
      case Direction.UP:
        next_position = Position(current_position.row-1, current_position.column)
        if next_position in obstacles:
          next_position = Position(current_position.row, current_position.column+1)
          print("Moving right:", next_position)
          return (next_position, Direction.RIGHT)
        print("Moving up:", next_position)
        return (next_position, Direction.UP)
      case Direction.RIGHT:
        next_position = Position(current_position.row, current_position.column+1)
        if next_position in obstacles:
          next_position = Position(current_position.row+1, current_position.column)
          print("Moving down:", next_position)
          return (next_position, Direction.DOWN)
        print("Moving right:", next_position)
        return (next_position, Direction.RIGHT)
      case Direction.DOWN:
        next_position = Position(current_position.row+1, current_position.column)
        if next_position in obstacles:
          next_position = Position(current_position.row, current_position.column-1)
          print("Moving left:", next_position)
          return (next_position, Direction.LEFT)
        print("Moving down:", next_position)
        return (next_position, Direction.DOWN)
      case Direction.LEFT:
        next_position = Position(current_position.row, current_position.column-1)
        if next_position in obstacles:
          next_position = Position(current_position.row-1, current_position.column)
          print("Moving up:", next_position)
          return (next_position, Direction.UP)
        print("Moving left:", next_position)
        return (next_position, Direction.LEFT)
      case default:
        raise ValueError("This direction is unknown:", default)

  direction = Direction.UP
  distinct_positions: List[Position] = [current_position]
  while current_position.row not in [0, map_size] and current_position.column not in [0, map_size]:
    next_position, direction = _move(obstacles=obstacles, current_position=current_position, direction=direction)
    if next_position not in distinct_positions:
      distinct_positions.append(next_position)
    current_position = next_position

  return distinct_positions

def get_distinct_positions(file_name: str) -> int:
  map: List[List[str]] = process_file(file_name=file_name, process=lambda x: [c for c in x.replace("\n", "")])
  current_position: Position
  obstacles: List[Position] = []
  for row in range(len(map)):
    for column in range(len(map[row])):
      if map[row][column] == "^":
        current_position = Position(row, column)
      elif map[row][column] == "#":
        obstacles.append(Position(row, column))
  
  assert len(map) == len(map[0])

  distinct_positions: List[Position] = _get_route(obstacles=obstacles, current_position=current_position, map_size=len(map)-1)

  return len(distinct_positions)



def main() -> None:
  file_name: str = "input/day6/input.txt"

  part_one = get_distinct_positions(file_name=file_name)
  print("Part one solution is:", part_one)

if __name__ == "__main__":
  main()