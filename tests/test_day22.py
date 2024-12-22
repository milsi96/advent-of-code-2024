from typing import Dict
import pytest

from advent_of_code.day22.main import get_next_secret_at, solve_part_one


@pytest.mark.parametrize(
    "secret, expected_secrets",
    [
        (
            123,
            {
                1: 15887950,
                2: 16495136,
                3: 527345,
                4: 704524,
                5: 1553684,
                6: 12683156,
                7: 11100544,
                8: 12249484,
                9: 7753432,
                10: 5908254,
            },
        )
    ],
)
def test_next_secrets(secret: int, expected_secrets: Dict[int, int]) -> None:
    for index, next_secret in expected_secrets.items():
        assert get_next_secret_at(secret=secret, at=index) == next_secret


@pytest.mark.parametrize(
    "file_name, rounds, expected", [("input/day22/example.txt", 2000, 37327623)]
)
def test_solve_part_one(file_name: str, rounds: int, expected: int) -> None:
    assert solve_part_one(file_name=file_name, rounds=rounds) == expected
