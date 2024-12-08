from shapely.geometry import Point
from typing import List, Set, Tuple
from itertools import groupby, combinations
from advent_of_code.utils.file_utils import process_file


def _get_offsets(p1: Point, p2: Point) -> Tuple[float, float]:
    length = p1.distance(p2)
    dx, dy = p2.x - p1.x, p2.y - p1.y
    unit_dx, unit_dy = dx / length, dy / length
    return unit_dx * length, unit_dy * length


def _get_locations(input: List[str]) -> List[Tuple[str, Point]]:
  locations: List[Tuple[str, Point]] = []
  for row in range(len(input)):
    for column in range(len(input[row])):
      if input[row][column] == ".":
        continue
      locations.append((str(input[row][column]), Point(row, column)))
  return locations


def get_first_level_antinodes(file_name: str) -> int:
  input: List[str] = process_file(file_name=file_name, process=lambda x: x.replace("\n", ""))
  input_size = len(input)
  locations = _get_locations(input=input)
  locations_by_frequency = groupby(sorted(locations, key=lambda e: e[0]), lambda location: location[0])

  antinodes: Set[Point] = set()
  for _, value in locations_by_frequency:
    location_combinations = list(combinations(map(lambda e: e[1], value), 2))
    for p1, p2 in location_combinations:
      offset_dx, offset_dy = _get_offsets(p1, p2)
      antinodes.add(Point(p1.x - offset_dx, p1.y - offset_dy))
      antinodes.add(Point(p2.x + offset_dx, p2.y + offset_dy))
  
  result = list(filter(lambda an: an.x >= 0 and an.y >= 0 and an.x < input_size and an.y < input_size, antinodes))
  return len(result)


def get_all_antinodes(file_name: str) -> int:
  input: List[str] = process_file(file_name=file_name, process=lambda x: x.replace("\n", ""))
  input_size = len(input)
  locations = _get_locations(input=input)
  locations_by_frequency = groupby(sorted(locations, key=lambda e: e[0]), lambda location: location[0])

  antinodes: Set[Point] = set()
  for _, points in locations_by_frequency:
    location_combinations = list(combinations(map(lambda e: e[1], points), 2))
    for p1, p2 in location_combinations:
      offset_dx, offset_dy = _get_offsets(p1, p2)
      backward_point = Point(p1.x - offset_dx, p1.y - offset_dy)
      antinodes.add(backward_point)
      start, end = backward_point, p1
      while start.x >= 0 and start.y >= 0:
        offset_dx, offset_dy = _get_offsets(start, end)
        backward_point = Point(backward_point.x - offset_dx, backward_point.y - offset_dy)
        antinodes.add(backward_point)
        end = start
        start = backward_point

      offset_dx, offset_dy = _get_offsets(p1, p2)
      forward_point = Point(p2.x + offset_dx, p2.y + offset_dy)
      antinodes.add(forward_point)
      start, end = p2, forward_point
      while end.x < input_size and end.y < input_size:
        offset_dx, offset_dy = _get_offsets(start, end)
        forward_point = Point(forward_point.x + offset_dx, forward_point.y + offset_dy)
        antinodes.add(forward_point)
        start = end
        end = forward_point

  result = list(filter(lambda an: an.x >= 0 and an.y >= 0 and an.x < input_size and an.y < input_size, antinodes))
  return len(set(result).union(set(map(lambda p: p[1], locations))))


def main() -> None:
  file_name: str = "input/day8/input.txt"

  antinodes = get_first_level_antinodes(file_name=file_name)
  print("Part one solution:", antinodes)

  all_antinodes = get_all_antinodes(file_name=file_name)
  print("Part two solution:", all_antinodes)



if __name__ == "__main__":
  main()