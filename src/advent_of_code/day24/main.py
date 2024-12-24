from dataclasses import dataclass
from enum import StrEnum
import re
from typing import Dict, List, Tuple

from advent_of_code.utils.file_utils import process_file


GATES_REGEX = r"([x-y]\d+): (\d{1})"
CONNECTION_REGEX = r"(.+) (OR|AND|XOR) (.+) -> (.+)"


class Operator(StrEnum):
    AND = "AND"
    OR = "OR"
    XOR = "XOR"

    def get_symbol(self) -> str:
        match self:
            case Operator.AND:
                return "and"
            case Operator.OR:
                return "or"
            case Operator.XOR:
                return "^"


@dataclass
class Connection:
    gate1: str
    gate2: str
    operator: Operator
    wire: str


def get_input(file_name: str) -> Tuple[Dict[str, int], List[Connection]]:
    lines = process_file(
        file_name=file_name, process=lambda line: line.replace("\n", "")
    )
    gates: Dict[str, int] = dict()
    connections: List[Connection] = list()

    for line in lines:
        if match := re.match(GATES_REGEX, line):
            gate, value = match.groups()
            gates[gate] = int(value)
        elif match := re.match(CONNECTION_REGEX, line):
            gate1, operator, gate2, wire = match.groups()
            connections.append(
                Connection(
                    gate1=gate1, gate2=gate2, operator=Operator(operator), wire=wire
                )
            )
            gates[wire] = -1

    return gates, connections


def get_output(gates: Dict[str, int], connections: List[Connection]) -> int:
    processed: List[int] = list()
    while not all(value != -1 for _, value in gates.items()):
        for i in range(len(connections)):
            if i in processed:
                continue

            if all(
                gates[gate] != -1
                for gate in [(connections[i].gate1), connections[i].gate2]
            ):
                result = eval(
                    f"gates[gate1] {connections[i].operator.get_symbol()} gates[gate2]",
                    {},
                    {
                        "gate1": connections[i].gate1,
                        "gate2": connections[i].gate2,
                        "gates": gates,
                    },
                )
                gates[connections[i].wire] = int(result)

    return get_number(gates=gates, target="z")


def get_number(gates: Dict[str, int], target: str) -> int:
    numbers = list(
        map(
            lambda entry: entry[1],
            sorted(
                filter(lambda entry: entry[0].startswith(target), gates.items()),
                reverse=True,
            ),
        )
    )
    return int("".join(list(map(str, numbers))), 2)


def solve_part_one(file_name: str) -> int:
    gates, connections = get_input(file_name=file_name)
    return get_output(gates=gates, connections=connections)


def main() -> None:
    file_name = "input/day24/input.txt"

    part_one = solve_part_one(file_name=file_name)
    print("Part one solution is", part_one)


if __name__ == "__main__":
    main()
