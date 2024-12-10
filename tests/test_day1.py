import pytest

from advent_of_code.day1.main import get_distances, get_similarity


@pytest.mark.parametrize("file_name, expected", [("input/day1/example.txt", 11)])
def test_distance_is_correct(file_name: str, expected: int) -> None:
    assert get_distances(file_name=file_name) == expected


@pytest.mark.parametrize("file_name, expected", [("input/day1/example.txt", 31)])
def test_similarity_is_correct(file_name: str, expected: int) -> None:
    assert get_similarity(file_name=file_name) == expected
