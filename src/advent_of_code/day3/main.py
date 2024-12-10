import re
from typing import Callable, List

from advent_of_code.utils.file_utils import process_file


def get_mul_sum(file_name: str) -> int:
    return _get_multiplications(
        file_name=file_name, process_input=lambda lines: "".join(lines)
    )


def get_mul_sum_donts(file_name: str) -> int:
    def _remove_donts_substrings(line: str) -> str:
        return re.sub(r"don't\(\).*?do\(\)", "", line)

    return _get_multiplications(
        file_name=file_name,
        process_input=lambda lines: _remove_donts_substrings(
            "".join(lines).replace("\n", "")
        ),
    )


def _get_multiplications(
    file_name: str, process_input: Callable[[List[str]], str]
) -> int:
    input: str = process_input(process_file(file_name=file_name, process=lambda x: x))
    multiplications = re.findall(r"mul\(\d+,\d+\)", input)
    numbers = [
        result.groups()
        for m in multiplications
        if (result := re.search(r"mul\((\d+),(\d+)\)", m)) is not None
    ]
    return sum(map(lambda t: int(t[0]) * int(t[1]), numbers))


def main() -> None:
    file_name: str = "input/day3/input.txt"

    first_part = get_mul_sum(file_name=file_name)
    print("Part one solution is", first_part)

    second_part = get_mul_sum_donts(file_name=file_name)
    print("Part one solution is", second_part)


if __name__ == "__main__":
    main()
