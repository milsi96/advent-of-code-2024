from functools import partial
from typing import Callable, List, Tuple, Union

import numpy as np
from advent_of_code.utils.file_utils import process_file
from dataclasses import dataclass
import re

BUTTON_A_REGEX = r"Button A: X\+(\d+), Y\+(\d+)"
BUTTON_B_REGEX = r"Button B: X\+(\d+), Y\+(\d+)"
PRIZE_REGEX = r"Prize: X=(\d+), Y=(\d+)"

BUTTON_A_TOKENS = 3
BUTTON_B_TOKENS = 1

MAX_PRESS = 100


@dataclass
class Button:
    dx: int
    dy: int


@dataclass
class Coordinate:
    x: int
    y: int


def get_input(file_name: str) -> List[Tuple[Button, Button, Coordinate]]:
    lines = process_file(
        file_name=file_name, process=lambda line: line.replace("\n", "")
    )
    button_a: Button
    button_b: Button
    prize: Coordinate

    machines: List[Tuple[Button, Button, Coordinate]] = list()
    for line in lines:
        if matches := re.match(BUTTON_A_REGEX, line):
            button_a = Button(int(matches.group(1)), int(matches.group(2)))
        elif matches := re.match(BUTTON_B_REGEX, line):
            button_b = Button(int(matches.group(1)), int(matches.group(2)))
        elif matches := re.match(PRIZE_REGEX, line):
            prize = Coordinate(int(matches.group(1)), int(matches.group(2)))
        else:
            machines.append((button_a, button_b, prize))

    machines.append((button_a, button_b, prize))

    return machines


def solve(
    file_name: str,
    convert_prize: Callable[[Coordinate], Coordinate],
    is_solution_valid: Callable[[float], bool],
) -> int:
    def solve_system(
        convert_prize: Callable[[Coordinate], Coordinate],
        is_solution_valid: Callable[[float], bool],
        claw_machine: Tuple[Button, Button, Coordinate],
    ) -> Union[int, None]:
        button_a, button_b, prize = claw_machine
        converted_prize = convert_prize(prize)

        solutions = np.linalg.solve(
            [[button_a.dx, button_b.dx], [button_a.dy, button_b.dy]],
            [converted_prize.x, converted_prize.y],
        )
        if not all(is_solution_valid(sol) for sol in solutions):
            return None

        int_solutions = list(map(lambda sol: sol.astype(int), np.round(solutions)))

        if (
            button_a.dx * int_solutions[0] + button_b.dx * int_solutions[1]
            != converted_prize.x
        ) or (
            button_a.dy * int_solutions[0] + button_b.dy * int_solutions[1]
            != converted_prize.y
        ):
            # to check wether solutions actually solve the equations:
            # it may happen that the solutions have decimal parts which is not admissable
            return None

        return int_solutions[0] * BUTTON_A_TOKENS + int_solutions[1] * BUTTON_B_TOKENS

    claw_machines = get_input(file_name=file_name)
    solve_system_partial = partial(solve_system, convert_prize, is_solution_valid)

    return sum(
        filter(
            lambda result: result is not None,
            map(lambda cm: solve_system_partial(cm), claw_machines),
        )
    )


def solve_part_one(file_name: str) -> int:
    return solve(
        file_name=file_name,
        convert_prize=lambda prize: prize,
        is_solution_valid=lambda sol: 0 <= sol <= MAX_PRESS,
    )


def solve_part_two(file_name: str) -> int:
    conversion = 10000000000000
    return solve(
        file_name=file_name,
        convert_prize=lambda prize: Coordinate(
            prize.x + conversion, prize.y + conversion
        ),
        is_solution_valid=lambda sol: 0 <= sol,
    )


def main() -> None:
    file_name: str = "input/day13/input.txt"

    part_one = solve_part_one(file_name=file_name)
    print("Part one solution is", part_one)

    part_two = solve_part_two(file_name=file_name)
    print("Part two solution is", part_two)


if __name__ == "__main__":
    main()
