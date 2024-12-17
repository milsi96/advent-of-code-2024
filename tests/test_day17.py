from typing import Dict, List
import pytest

from advent_of_code.day17.main import A, B, C, solve_part_one, run_program


@pytest.mark.parametrize(
    "file_name, expected", [("input/day17/example.txt", "4,6,3,5,6,3,5,2,1,0")]
)
def test_solve_part_one(file_name: str, expected: str) -> None:
    assert solve_part_one(file_name=file_name) == expected


@pytest.mark.parametrize(
    "registers, program, condition",
    [
        ({B: 0, C: 9}, [2, 6], "registers[B] == 1"),
        ({A: 10}, [5, 0, 5, 1, 5, 4], "out == '0,1,2'"),
        ({B: 29}, [1, 7], "registers[B] == 26"),
        ({B: 2024, C: 43690}, [4, 0], "registers[B] == 44354"),
        (
            {A: 2024},
            [0, 1, 5, 4, 3, 0],
            "registers[A] == 0 and out == '4,2,5,6,7,7,7,7,3,1,0'",
        ),
    ],
)
def test_run_program(
    registers: Dict[str, int], program: List[int], condition: str
) -> None:
    out = run_program(registers=registers, program=program)  # noqa: F841
    assert eval(condition)
