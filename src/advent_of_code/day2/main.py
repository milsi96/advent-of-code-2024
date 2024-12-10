from typing import Callable, List

from advent_of_code.utils.file_utils import process_file


def _get_input(file_name: str, process: Callable[[str], List[int]]) -> List[List[int]]:
    return process_file(file_name=file_name, process=process)


def _process_into_report(line: str) -> List[int]:
    return [int(n) for n in line.split(" ")]


def _is_report_valid(report: List[int]) -> bool:
    valid_increasing = all(
        1 <= report[i] - report[i - 1] <= 3 for i in range(1, len(report))
    )
    valid_decreasing = all(
        1 <= report[i - 1] - report[i] <= 3 for i in range(1, len(report))
    )
    return valid_increasing or valid_decreasing


def get_safe_reports(file_name: str) -> int:
    reports: List[List[int]] = _get_input(
        file_name=file_name, process=_process_into_report
    )
    return sum([_is_report_valid(report) for report in reports])


def get_tolerated_safe_reports(file_name: str) -> int:
    reports: List[List[int]] = _get_input(
        file_name=file_name, process=_process_into_report
    )
    result = [
        any(
            _is_report_valid(report=option)
            for option in _get_bad_level_options(report=report)
        )
        for report in reports
    ]
    return sum(result)


def _get_bad_level_options(report: List[int]) -> List[List[int]]:
    result: List[List[int]] = []
    for i in range(len(report)):
        option = report.copy()
        option.pop(i)
        result.append(option)
    return result


def main() -> None:
    file_name: str = "input/day2/input.txt"

    safe_reports = get_safe_reports(file_name=file_name)
    print("Part one solution is", safe_reports)

    tolerated_reports = get_tolerated_safe_reports(file_name=file_name)
    print("Part two solution is", tolerated_reports)


if __name__ == "__main__":
    main()
