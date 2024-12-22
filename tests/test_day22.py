from typing import Dict, List, Tuple
import pytest

from advent_of_code.day22.main import (
    get_buyer_sequence,
    get_changes,
    get_differences,
    solve_part_one,
    solve_part_two,
)


@pytest.mark.parametrize(
    "secret, expected_secrets",
    [
        (
            123,
            [
                123,
                15887950,
                16495136,
                527345,
                704524,
                1553684,
                12683156,
                11100544,
                12249484,
                7753432,
                5908254,
            ],
        )
    ],
)
def test_next_secrets(secret: int, expected_secrets: List[int]) -> None:
    assert get_buyer_sequence(secret=secret, rounds=11) == expected_secrets


@pytest.mark.parametrize(
    "file_name, rounds, expected", [("input/day22/example.txt", 2000, 37327623)]
)
def test_solve_part_one(file_name: str, rounds: int, expected: int) -> None:
    assert solve_part_one(file_name=file_name, rounds=rounds) == expected


@pytest.mark.parametrize(
    "file_name, rounds, expected", [("input/day22/example2.txt", 2000, 23)]
)
def test_solve_part_two(file_name: str, rounds: int, expected: int) -> None:
    assert solve_part_two(file_name=file_name, rounds=rounds) == expected


@pytest.mark.parametrize(
    "buyer, rounds, expected", [(123, 10, (-3, 6, -1, -1, 0, 2, -2, 0, -2))]
)
def test_get_differences(buyer: int, rounds: int, expected: Tuple[int, ...]) -> None:
    assert get_differences(get_buyer_sequence(rounds=rounds, secret=buyer)) == expected


@pytest.mark.parametrize("buyer, rounds, expected", [(123, 10, {(-1, -1, 0, 2): 6})])
def test_get_changes(
    buyer: int, rounds: int, expected: Dict[Tuple[int, ...], int]
) -> None:
    for sequence, price in expected.items():
        assert get_changes(buyer=buyer, rounds=rounds)[sequence] == price
