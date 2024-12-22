from collections import defaultdict
from itertools import starmap
from typing import DefaultDict, Dict, List, Tuple, TypeAlias

from advent_of_code.utils.file_utils import process_file

from functools import partial

Sequence: TypeAlias = Tuple[int, int, int, int]


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


def get_buyer_sequence(rounds: int, secret: int) -> List[int]:
    next_secret_at = partial(get_next_secret_at, secret)
    return list(map(next_secret_at, range(rounds)))


def solve_part_one(file_name: str, rounds: int) -> int:
    numbers = [[number, rounds] for number in get_numbers(file_name=file_name)]
    return sum(starmap(get_next_secret_at, numbers))


def get_differences(sequence: List[int]) -> Tuple[int, ...]:
    result: List[int] = list()
    last_digits = list(map(int, map(lambda n: n[-1], map(str, sequence))))
    for i in range(1, len(last_digits)):
        result.append(last_digits[i] - last_digits[i - 1])
    return tuple(result)


def get_changes(rounds: int, buyer: int) -> Dict[Tuple[int, ...], int]:
    current_round: int = 0
    result: Dict[Tuple[int, ...], int] = dict()
    secret = buyer

    print("Getting changes for buyer", buyer)

    while current_round <= rounds:
        sequence = get_buyer_sequence(5, secret)
        differences = get_differences(sequence)

        if differences not in result.keys():
            result[differences] = int(str(sequence[-1])[-1])

        secret = sequence[1]
        current_round += 1

    return result


def solve_part_two(file_name: str, rounds: int) -> int:
    buyers: List[int] = get_numbers(file_name=file_name)
    changes_for_rounds = partial(get_changes, rounds)
    total_prices: DefaultDict[Tuple[int, ...], int] = defaultdict(int)

    for changes in map(changes_for_rounds, buyers):
        for sequence, price in changes.items():
            total_prices[sequence] += price

    return max(total_prices.values())


def main() -> None:
    file_name = "input/day22/input.txt"

    part_one = solve_part_one(file_name=file_name, rounds=2000)
    print("Part one solution is", part_one)

    part_two = solve_part_two(file_name=file_name, rounds=2000)
    print("Part two solution is", part_two)


if __name__ == "__main__":
    main()
