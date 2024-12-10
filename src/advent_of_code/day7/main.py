from dataclasses import dataclass
from typing import Callable, List, Tuple
from advent_of_code.utils.file_utils import process_file


@dataclass
class Equation:
    result: float
    numbers: List[int]


def _process_equations(input: str) -> Equation:
    result = float(input.split(":")[0])
    numbers = list(map(int, input.replace("\n", "").split(":")[1].strip().split(" ")))
    return Equation(result=result, numbers=numbers)


def get_valid_equations_sum(file_name: str) -> Tuple[int, int]:
    equations: List[Equation] = process_file(
        file_name=file_name, process=_process_equations
    )

    def sum_op(num, acc):
        return num + acc

    def mul_op(num, acc):
        return num * acc

    def comb_op(num, acc):
        return int(f"{acc}{num}")

    valid_equations = [
        e
        for e in equations
        if _is_valid(
            equation=Equation(e.result, e.numbers[1:]),
            acc=e.numbers[0],
            operators=[sum_op, mul_op],
        )
    ]
    valid_equations_combination = [
        e
        for e in equations
        if _is_valid(
            equation=Equation(e.result, e.numbers[1:]),
            acc=e.numbers[0],
            operators=[sum_op, mul_op, comb_op],
        )
    ]
    return (
        sum(map(lambda e: e.result, valid_equations)),
        sum(map(lambda e: e.result, valid_equations_combination)),
    )


def _is_valid(
    equation: Equation, acc: int, operators: List[Callable[[int, int], int]]
) -> bool:
    if equation.result < acc or (len(equation.numbers) == 0 and equation.result != acc):
        return False
    elif equation.result == acc and len(equation.numbers) == 0:
        return True
    else:
        return any(
            _is_valid(
                equation=Equation(result=equation.result, numbers=equation.numbers[1:]),
                acc=op(equation.numbers[0], acc),
                operators=operators,
            )
            for op in operators
        )


def main() -> None:
    file_name: str = "input/day7/input.txt"

    part_one, part_two = get_valid_equations_sum(file_name=file_name)
    print("Part one solution is", int(part_one))
    print("Part two solution is", int(part_two))


if __name__ == "__main__":
    main()
