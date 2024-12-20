from functools import partial
import re
from typing import Dict, Generator, List, Tuple

from advent_of_code.utils.file_utils import process_file

A: str = "A"
B: str = "B"
C: str = "C"


def get_input(file_name: str) -> Tuple[Dict[str, int], List[int]]:
    lines = process_file(
        file_name=file_name, process=lambda line: line.replace("\n", "")
    )

    registers: Dict[str, int] = dict()
    program: List[int] = list()

    register_regex = r"Register ([A-C]): (\d+)"
    program_regex = r"Program: (.+)"
    for line in lines:
        if m := re.match(register_regex, line):
            register, value = m.groups()
            registers[register] = int(value)
        elif m := re.match(program_regex, line):
            values = list(map(int, m.group(1).split(",")))
            program.extend(values)

    return registers, program


def division(numerator: int, denominator: int) -> int:
    return numerator // denominator


def bitwise_xor(op1: int, op2: int) -> int:
    return op1 ^ op2


def modulo(modulo: int, op: int) -> int:
    return op % modulo


def get_combo_operand(registers: Dict[str, int], operand: int) -> int:
    if operand in [*(range(0, 4))]:
        return operand
    elif operand == 4:
        return registers[A]
    elif operand == 5:
        return registers[B]
    elif operand == 6:
        return registers[C]
    else:
        raise ValueError("7 is not supported")


def run_program(
    registers: Dict[str, int], program: List[int]
) -> Generator[int, None, None]:
    modulo_8, combo_operand = partial(modulo, 8), partial(get_combo_operand, registers)
    instruction_pointer: int = 0

    while True:
        instruction = program[instruction_pointer]
        operand = program[instruction_pointer + 1]
        match instruction:
            case 0:
                registers[A] = division(
                    numerator=registers[A], denominator=pow(2, combo_operand(operand))
                )
            case 1:
                registers[B] = bitwise_xor(op1=registers[B], op2=operand)
            case 2:
                registers[B] = modulo_8(op=combo_operand(operand))
            case 3:
                if registers[A] != 0:
                    instruction_pointer = operand
                    continue
            case 4:
                registers[B] = bitwise_xor(op1=registers[B], op2=registers[C])
            case 5:
                yield modulo_8(op=combo_operand(operand))
            case 6:
                registers[B] = division(
                    numerator=registers[A], denominator=pow(2, combo_operand(operand))
                )
            case 7:
                registers[C] = division(
                    numerator=registers[A], denominator=pow(2, combo_operand(operand))
                )

        instruction_pointer += 2
        if instruction_pointer > len(program) - 1:
            break


def solve_part_two(file_name: str) -> int:
    registers, program = get_input(file_name=file_name)
    tryout: int = 0

    while True:
        registers[A] = tryout
        program_index = 0
        acc: List[int] = list()
        for out in run_program(registers=registers, program=program):
            if out != program[program_index] or program_index > len(program):
                break
            acc.append(out)
            program_index += 1
        if acc == program:
            return tryout
        tryout += 1


def solve_part_one(file_name: str) -> str:
    return ",".join(list(map(str, run_program(*get_input(file_name=file_name)))))


def main() -> None:
    file_name: str = "input/day17/input.txt"

    out = solve_part_one(file_name=file_name)
    print("Part one solution is", out)

    # This does not work with the actual input
    # target_a_value = solve_part_two(file_name=file_name)
    # print("Part two solution is", target_a_value)


if __name__ == "__main__":
    main()
