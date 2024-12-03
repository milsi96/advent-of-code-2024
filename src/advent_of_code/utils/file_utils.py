from typing import Callable, List, TypeVar

T = TypeVar('T')

def process_file(file_name: str, process: Callable[[str], T]) -> List[T]: 
  with open(file_name, "r") as file:
    return list(map(process, file.readlines()))