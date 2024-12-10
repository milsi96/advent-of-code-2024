from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def process_file(file_name: str, process: Callable[[str], T]) -> list[T]:
    with open(file_name) as file:
        return list(map(process, file.readlines()))
