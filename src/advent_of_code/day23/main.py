from collections import defaultdict
from functools import partial
from itertools import combinations
from typing import DefaultDict, Generator, List, Set, Tuple, TypeAlias

from advent_of_code.utils.file_utils import process_file


ComputerTriple: TypeAlias = Tuple[str, str, str]


def get_connections(file_name: str) -> DefaultDict[str, List[str]]:
    tuples = process_file(
        file_name=file_name,
        process=lambda line: ((pcs := line.replace("\n", "").split("-"))[0], pcs[1]),
    )
    connections: DefaultDict[str, List[str]] = defaultdict(list)
    for tup in tuples:
        computer, link = tup
        connections[computer].append(link)
        connections[link].append(computer)

    return connections


def get_possible_combination(
    connections: DefaultDict[str, List[str]],
) -> Generator[ComputerTriple, None, None]:
    for combination in combinations(connections.keys(), 3):
        yield combination


def is_combination_valid(
    connections: DefaultDict[str, List[str]], combination: ComputerTriple
) -> bool:
    first, second, third = combination

    if all(el in connections.get(first, list()) for el in [second, third]):
        if all(el in connections.get(second, list()) for el in [first, third]):
            if all(el in connections.get(third, list()) for el in [first, second]):
                return True

    return False


def solve_part_one(file_name: str, letter_filter: str) -> int:
    connections = get_connections(file_name=file_name)
    triples: Set[ComputerTriple] = set()
    is_valid = partial(is_combination_valid, connections)

    for combination in get_possible_combination(connections=connections):
        if is_valid(combination=combination) and any(
            [el[0] == letter_filter for el in [*combination]]
        ):
            triples.add(combination)

    return len(triples)


def main() -> None:
    file_name: str = "input/day23/input.txt"

    part_one = solve_part_one(file_name=file_name, letter_filter="t")
    print("Part one solution is", part_one)


if __name__ == "__main__":
    main()
