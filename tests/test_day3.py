import pytest

from advent_of_code.day3.main import get_mul_sum, get_mul_sum_donts


@pytest.mark.parametrize("file_name, expected", [("input/day3/example.txt", 161)])
def test_multiplication_result_correct(file_name: str, expected: int) -> None:
    assert get_mul_sum(file_name) == expected


@pytest.mark.parametrize("file_name, expected", [("input/day3/example2.txt", 48)])
def test_apply_donts(file_name: str, expected: int) -> None:
    assert get_mul_sum_donts(file_name) == expected
