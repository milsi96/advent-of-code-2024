from typing import List
import pytest

from advent_of_code.day22.main import get_buyer_sequence, solve_part_one


@pytest.mark.parametrize(
    "secret, expected_secrets",
    [
        (
            123,
            [
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
    assert get_buyer_sequence(secret=secret, rounds=10) == expected_secrets


@pytest.mark.parametrize(
    "file_name, rounds, expected", [("input/day22/example.txt", 2000, 37327623)]
)
def test_solve_part_one(file_name: str, rounds: int, expected: int) -> None:
    assert solve_part_one(file_name=file_name, rounds=rounds) == expected
