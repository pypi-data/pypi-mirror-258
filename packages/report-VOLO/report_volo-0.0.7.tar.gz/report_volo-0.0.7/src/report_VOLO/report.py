import argparse
from datetime import datetime, timedelta
from pathlib import Path
import re
import copy


class FileNotFound(Exception):
    pass


class ReportInvalidOrder(Exception):
    pass


class Record:
    regex_abbr = re.compile(r"(^[A-Z]{3})_(\w+\s\w+)_([A-Z\s]+$)")
    regex_log = re.compile(r"(^[A-Z]{3})(\d+-\d+-\d+_\d+:\d+:\d+.\d+)")

    def __init__(
        self,
        abbr: str = None,
        driver: str = None,
        team: str = None,
        start: datetime = None,
        end: datetime = None,
        error: str = None,
    ):
        self.abbr = abbr
        self.driver = driver
        self.team = team
        self._start = start
        self._end = end
        self.error = error

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        if isinstance(value, datetime):
            if not self.end or self.end > value:
                self._start = value
            else:
                self.error = "Invalid start time: must be before the end time"
        else:
            self.error = "start() expects a datetime object"

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        if isinstance(value, datetime):
            if not self.start or self.start < value:
                self._end = value
            else:
                self.error = "Invalid end time: must be after the start time"
        else:
            self.error = "end() expects a datetime object"

    @property
    def result(self):
        return self.end - self.start if self.start and self.end else None

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Record):
            return (
                self.abbr == value.abbr
                and self.team == value.team
                and self.driver == value.driver
                and self._end == value.end
                and self._start == value.start
                and self.error == value.error
            )
        else:
            return NotImplemented

    def __ne__(self, value: object) -> bool:
        x = self.__eq__(value)
        return not x if x is not NotImplemented else NotImplemented

    def __repr__(self):
        return f"Record({self.driver}, {self.team}, {self.start}, {self.end}, {self.error})"

    def __str__(self):
        return f"{self.driver:<20} | {self.team:<30} | {self.result if not self.error else self}"

    @staticmethod
    def read_abbr(
        path: str | Path,
        records_dict: dict[str, "Record"] = None,
        abbr_file: str = "abbreviations.txt",
    ) -> dict[str, "Record"]:
        """
        Validate the file path, extract abbreviations, and save them in a deep copy of the data
        dictionary, retaining only lines that match the regular expression pattern.
        Args:
            path: Path to the directory containing abbreviations file.
            records_dict: Optional dictionary to populate (defaults to empty).
            abbr_file: Name of the abbreviations file (defaults to "abbreviations.txt").

        Returns:
            Deep copy of the dictionary with parsed abbreviations.

        Raises:
            FileNotFound: If the specified file is not found.
        """
        records_dict_copy = (
            copy.deepcopy(records_dict) if records_dict is not None else {}
        )
        file_path = Path(path) / abbr_file
        if not file_path.exists():
            raise FileNotFound(f"{file_path} not found")

        with open(file_path, "r") as file:
            for line_index, line in enumerate(file, start=1):
                if Record.regex_abbr.match(line):
                    abbr, driver, team = line.strip().split("_")
                    records_dict_copy[abbr] = Record(driver=driver, team=team)
                else:
                    abbr_error = f"Bad data: {abbr_file}, line: {line_index}"
                    records_dict_copy[abbr_error] = Record(error=abbr_error)
        return records_dict_copy

    @staticmethod
    def read_logs(
        path: str | Path,
        records_dict: dict[str, "Record"] = None,
        start_file: str = "start.log",
        end_file: str = "end.log",
    ) -> dict[str, "Record"]:
        """
        Validate the file paths, extract start and end data, and save a deep copy of the data
        in dictionary if record keys are available, retaining lines that match the reg. ex. pattern.

        Args:
            path: Path to the directory containing logs files.
            records_dict: Optional dictionary to populate (defaults to empty).
            start_file: Name of the start file (defaults to "start.log").
            end_file: Name of the end file (defaults to "end.log").

        Returns:
            Deep copy of the dictionary with parsed start and end logs.

        Raises:
            FileNotFound: If the specified start or end file is not found.
        """
        records_dict_copy = (
            copy.deepcopy(records_dict) if records_dict is not None else {}
        )

        file_info = [
            (start_file, "start", "start", datetime.fromisoformat),
            (end_file, "end", "end", datetime.fromisoformat),
        ]

        for file_name, log_type, record_attr, parse_time_func in file_info:
            file_path = Path(path) / file_name
            if not file_path.exists():
                raise FileNotFound(f"{file_path} not found")

            with open(file_path, "r") as file:
                for line_index, line in enumerate(file, start=1):
                    if match := re.match(Record.regex_log, line.strip()):
                        record_key, log_time = match.groups()
                        if record_key in records_dict_copy:
                            record = records_dict_copy[record_key]
                            if not record.start and record_attr == "start":
                                record.start = parse_time_func(log_time)
                            elif not record.end and record_attr == "end":
                                record.end = parse_time_func(log_time)
                        else:
                            log_error = f"Bad abbr: {record_key}, line: {line_index}, file: {file_name}"
                            records_dict_copy[log_error] = Record(error=log_error)
                    else:
                        log_error = f"Bad data: {file_name}, line: {line_index}"
                        records_dict_copy[log_error] = Record(error=log_error)

        return records_dict_copy

    @staticmethod
    def build_report(
        path: str | Path,
        order: str = "asc",
    ) -> tuple[list["Record"], list["Record"]]:
        """
        Compiles a report summarizing valid and invalid records based on provided logs and abbreviations.

        Reads log files (end.log and start.log) and parses abbreviations from a text file (abbreviations.txt).
        Validates the order operator and sorts the data in ascending or descending order.

        Args:
            path: Path to the directory containing the log files and abbreviations text file.
            order: Sort order for records, 'asc' (ascending) or 'desc' (descending). Defaults to 'asc'.

        Returns:
            Tuple with two lists: good_record as valid list and bad_records as list of broken records.
        """
        good_records, bad_records = [], []

        try:
            if order not in ["asc", "desc"]:
                raise ReportInvalidOrder(
                    f"Invalid sorting order '{order}'. Valid options are: asc, desc"
                )

            records_dict = Record.read_abbr(path=path)
            records_dict = Record.read_logs(path=path, records_dict=records_dict)

            for rec in records_dict.values():
                (bad_records if rec.error else good_records).append(rec)

            multiplier = 1 if order == "asc" else -1
            good_records.sort(key=lambda x: multiplier * (x.result or timedelta(0)))

        except ReportInvalidOrder as e:
            print(str(e))
            return [], []

        return good_records, bad_records

    @staticmethod
    def print_report(good_records, bad_records, border_line: int = 15):
        """
        Print a formatted report based on a list of ordered results.

        Args:
            good_records - list of valid records in dict
            bad_records - list of invalid records in dict
        """

        result_string = ""
        line_count = 0

        for num, rec in enumerate(good_records + bad_records, start=1):
            driver = rec.driver if rec.driver is not None else "Missing Data"
            team = rec.team if rec.team is not None else "Missing Data"
            result = rec.result if not rec.error else rec.error

            record_str = f"{num:2}. {driver:<20} | {team:<30} | {result}"

            result_string += record_str + "\n"

            if num == border_line:
                result_string += "-" * 75 + "\n"
            line_count += 1

        return result_string

    @classmethod
    def cli(cls, args_list=None) -> argparse.Namespace:
        """
        Parses command-line arguments and orchestrates the report generation process.

        Args:
            args_list (list): List of strings representing command-line arguments.

        Returns:
            argparse.Namespace: Parsed command-line arguments.

        Example:
            Record.cli(["--files", "../data", "--asc", "--driver", "Sergey Sirotkin"])
        """
        parser = argparse.ArgumentParser(description="Build Monaco report")

        parser.add_argument("--files", required=True, help="Path to folder")

        group = parser.add_mutually_exclusive_group()
        group.add_argument("--asc", action="store_true", help="Ascending order sort")
        group.add_argument("--desc", action="store_true", help="Descending order sort")
        parser.add_argument("--driver", help="Show statistics for a specific driver")

        args = parser.parse_args(args_list)

        args.sort = "asc" if args.asc else "desc"

        return args


if __name__ == "__main__":
    args = Record.cli()

    good_records, bad_records = Record.build_report(args.files, args.sort)

    if args.driver:
        good_records = [rec for rec in good_records if rec.driver == args.driver]
        bad_records = [rec for rec in bad_records if rec.driver == args.driver]

    print(Record.print_report(good_records, bad_records))
