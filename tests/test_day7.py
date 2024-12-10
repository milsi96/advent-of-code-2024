import pytest

from advent_of_code.day7.main import get_valid_equations_sum


@pytest.mark.parametrize(
    "file_name, expected, expected_with_combination",
    [("input/day7/example.txt", 3749, 11387)],
)
def test_valid_equations(
    file_name: str, expected: int, expected_with_combination: int
) -> None:
    assert get_valid_equations_sum(file_name=file_name) == (
        expected,
        expected_with_combination,
    )
