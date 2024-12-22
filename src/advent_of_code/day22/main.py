from itertools import starmap
from typing import List

from advent_of_code.utils.file_utils import process_file

from functools import partial


def get_numbers(file_name: str) -> List[int]:
    return process_file(
        file_name=file_name, process=lambda line: int(line.replace("\n", ""))
    )


def get_next_secret_at(secret: int, at: int) -> int:
    def get_next_secret(from_number: int) -> int:
        def multiply(multiplier: int, number: int) -> int:
            return number * multiplier

        def divide(divisor: int, number: int) -> int:
            return number // divisor

        def mix(n1: int, n2: int) -> int:
            return n1 ^ n2

        def prune(number: int) -> int:
            return number % 16777216

        multiply_by_64 = partial(multiply, 64)
        divide_by_32 = partial(divide, 32)
        multiply_by_2048 = partial(multiply, 2048)

        secret = from_number
        secret = prune(mix(n1=multiply_by_64(secret), n2=secret))
        secret = prune(mix(n1=divide_by_32(secret), n2=secret))
        secret = prune(mix(n1=multiply_by_2048(secret), n2=secret))

        return secret

    result: int = secret
    for _ in range(at):
        result = get_next_secret(from_number=result)
    return result


def solve_part_one(file_name: str, rounds: int) -> int:
    numbers = [[number, rounds] for number in get_numbers(file_name=file_name)]
    return sum(starmap(get_next_secret_at, numbers))


def main() -> None:
    file_name = "input/day22/input.txt"

    part_one = solve_part_one(file_name=file_name, rounds=2000)
    print("Part one solution is", part_one)


if __name__ == "__main__":
    main()
