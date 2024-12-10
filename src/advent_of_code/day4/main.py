import numpy as np
from typing import List

from advent_of_code.utils.file_utils import process_file


def _reverse_line(line: str) -> str:
    return line[::-1]


def _transpose_matrix(matrix: List[List[str]]) -> List[List[str]]:
    return np.array(matrix).transpose().tolist()


def _get_diagonals(matrix: List[List[str]]) -> List[List[str]]:
    return [
        np.array(matrix).diagonal(offset=offset).tolist()
        for offset in range(len(matrix), -len(matrix) - 1, -1)
    ]


def _get_anti_diagonals(matrix: List[List[str]]) -> List[List[str]]:
    return _get_diagonals(np.fliplr(np.array(matrix)).tolist())


def _get_occurrences(matrix: List[List[str]], word: str) -> int:
    return sum(
        [
            "".join(line).count(word) + _reverse_line(line="".join(line)).count(word)
            for line in matrix
        ]
    )


def get_total_occurrences(file_name: str, word: str) -> int:
    input: List[List[str]] = process_file(
        file_name=file_name, process=lambda x: list(x.replace("\n", ""))
    )
    return (
        _get_occurrences(matrix=input, word=word)
        + _get_occurrences(matrix=_transpose_matrix(matrix=input), word=word)
        + _get_occurrences(matrix=_get_diagonals(matrix=input), word=word)
        + _get_occurrences(matrix=_get_anti_diagonals(matrix=input), word=word)
    )


def get_total_X(file_name: str, word: str) -> int:
    matrix: List[List[str]] = process_file(
        file_name=file_name, process=lambda x: list(x.replace("\n", ""))
    )
    result: int = 0
    for row in range(1, len(matrix) - 1):
        for column in range(1, len(matrix[row]) - 1):
            if matrix[row][column] != "A":
                continue
            diagonal = "".join(
                [
                    matrix[row - 1][column - 1],
                    matrix[row][column],
                    matrix[row + 1][column + 1],
                ]
            )
            anti_diagonal = "".join(
                [
                    matrix[row + 1][column - 1],
                    matrix[row][column],
                    matrix[row - 1][column + 1],
                ]
            )
            if (word in [diagonal, _reverse_line(diagonal)]) and (
                word in [anti_diagonal, _reverse_line(anti_diagonal)]
            ):
                result += 1

    return result


def main() -> None:
    file_name: str = "input/day4/input.txt"

    part_one = get_total_occurrences(file_name=file_name, word="XMAS")
    print("Part one solution is", part_one)

    part_two = get_total_X(file_name=file_name, word="MAS")
    print("Part two solution is:", part_two)


if __name__ == "__main__":
    main()
