import argparse
from datetime import datetime
from tabulate import tabulate


def process_abb() -> dict:
    """
    Read abbreviations from file and return them as a dictionary.

    :abb: a file with abbreviations
    :data: dictionary with abbreviations, names and cars
    :return: a dictionary with abbreviation as key, dictionary as value with name as key and car brand as value
    """
    abb = readfile("../race_data/abbreviations.txt")
    data = {
        abb: {name: car for name, car in zip(line.split("_")[1:], line.split("_")[2:])}
        for abb, line in zip([i.split("_")[0] for i in abb], abb)
    }
    return data


def format_time(time_diff: dict) -> dict:
    """
    Format time from dictionary with a abbreviation as key and timedelta as value to dictionary with
    abbreviation as value and human-readable time as value, sorted by time

    :param time_diff: a dict with abbreviation as key and timedelta as value
    :type time_diff: dict
    :return: dictionary with abbreviation as key and human-readable time as value
    """
    time_diff_formatted = {
        key: f"{value.seconds // 60}:{value.seconds % 60:02}.{value.microseconds // 1000:03}"
        for key, value in time_diff.items()
    }
    sorted_by_time = dict(sorted(time_diff_formatted.items(), key=lambda x: x[1]))
    return sorted_by_time


def readfile(filepath: str) -> list[str]:
    """
    Open a file and return a list of strings

    :param filepath: a path to the file
    :type filepath: str
    :return: a list of strings
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read().splitlines()


def process_time() -> dict:
    """
    Process time from dictionary

    :start_log: the start time of the race
    :end_log: the end time of the race
    :start_time: a dictionary with abbreviation as key and start time as value
    :end_time: a dictionary with abbreviation as key and end time as value
    :time_diff: a dictionary with abbreviation as key and timedelta as value

    :return: dict with abbreviation as key and timedelta as value
    """
    start_log = readfile("../race_data/start.log")
    end_log = readfile("../race_data/end.log")

    start_time = {abb[:3]: t[-12:] for abb, t in zip(start_log, start_log)}
    end_time = {abb[:3]: t[-12:] for abb, t in zip(end_log, end_log)}

    time_diff = {
        key: (
                datetime.strptime(end_time[key], "%H:%M:%S.%f")
                - datetime.strptime(start_time[key], "%H:%M:%S.%f")
        )
        for key in start_time
    }
    return format_time(time_diff)


def build_report(driver: str = None) -> list[list]:
    """
    Build a report with all the data in the race_data directory and return it as a list

    :param driver: the name of the driver, optional
    :type driver: str
    :table: list
    :time: a dictionary with abbreviation as key and human-readable time as value
    :data: a dictionary with abbreviation, driver's names and cars
    :return: a list with all the data in the race_data
    """
    table = []
    time = process_time()
    data = process_abb()
    if driver is not None:
        for name, time in time.items():
            if list(data[name].keys())[0] == driver:
                table.append(
                    [list(data[name].keys())[0], list(data[name].values())[0], time]
                )
    else:
        for name, time in time.items():
            table.append(
                [list(data[name].keys())[0], list(data[name].values())[0], time]
            )
    return table


def arg_parser() -> argparse.ArgumentParser:
    """
    Parse command line arguments

    :return: parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        prog="report.py",
        description="Make a report of race from 2 data files",
        usage="type report.py --files race_data --asc (or --desc) for show list of drivers in order (default ascending). "
              'type report.py --files race_data --driver "Sebastian Vettel" for show statistic about driver',
        conflict_handler="error",
    )
    parser.add_argument("--files", type=str, help="path of data files", required=True)
    parser.add_argument(
        "--asc",
        action="store_true",
        help="show statistic about drivers in ascending order  (default)",
        required=False,
    )
    parser.add_argument(
        "--desc",
        action="store_true",
        help="show statistic about drivers in descending order",
        required=False,
    )
    parser.add_argument("--driver", type=str, help="show statistic about driver")

    return parser


def print_report() -> str | None:
    """
    Print a report of race from data to the cli using tabulate library for pretty-print data
    """
    table = build_report()
    parser = arg_parser()
    args, unknown = parser.parse_known_args()
    if args.driver:
        one_driver = build_report(args.driver)
        if one_driver:
            print(tabulate(one_driver, tablefmt="fancy_grid"))
        else:
            print(f"There is no driver with name {args.driver}")
    elif args.desc:
        print(
            tabulate(
                table[::-1],
                tablefmt="fancy_grid",
                showindex=range(1, len(table) + 1)[::-1],
            )
        )
    elif args.asc:
        print(
            tabulate(table, tablefmt="fancy_grid", showindex=range(1, len(table) + 1))
        )
    else:
        return parser.print_help()


def main():
    """
    Main function
    """
    print_report()


if __name__ == "__main__":
    main()
