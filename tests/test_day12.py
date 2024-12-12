from typing import List, Tuple
import pytest

from advent_of_code.day12.main import get_perimeter, get_regions, get_total_price


@pytest.mark.parametrize(
    "file_name, expected_perimeters",
    [
        (
            "input/day12/example.txt",
            [("A", 10), ("B", 8), ("C", 10), ("D", 4), ("E", 8)],
        ),
        ("input/day12/example2.txt", [("X", 16), ("O", 36)]),
    ],
)
def test_get_regions_perimeter(
    file_name: str, expected_perimeters: List[Tuple[str, int]]
) -> None:
    assert len((regions := get_regions(file_name=file_name)).keys()) == len(
        expected_perimeters
    )
    for region, perimeter in expected_perimeters:
        assert region in regions.keys()
        assert perimeter == get_perimeter(regions[region])


@pytest.mark.parametrize(
    "file_name, expected",
    [
        ("input/day12/example.txt", 140),
        ("input/day12/example2.txt", 772),
        ("input/day12/example3.txt", 1930),
    ],
)
def test_total_price(file_name: str, expected: int) -> None:
    assert get_total_price(file_name=file_name) == expected
