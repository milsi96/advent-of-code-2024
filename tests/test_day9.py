import pytest

from advent_of_code.day9.main import move_files, remove_empty_spaces


@pytest.mark.parametrize("file_name, expected", [("input/day9/example.txt", 1928)])
def test_remove_empty_spaces_checksum(file_name: str, expected: int) -> None:
    assert remove_empty_spaces(file_name=file_name) == expected


@pytest.mark.parametrize("file_name, expected", [("input/day9/example.txt", 2858)])
def test_move_files_checksum(file_name: str, expected: int) -> None:
    assert move_files(file_name=file_name) == expected
