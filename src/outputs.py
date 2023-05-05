import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import List

from prettytable import PrettyTable

from constants import DATETIME_FORMAT


def control_output(results: List[List[str]], cli_args) -> None:
    output = cli_args.output
    if output == 'pretty':
        pretty_output(results)
    elif output == 'file':
        file_output(results, cli_args)
    else:
        default_output(results)


def default_output(results: List[List[str]]) -> None:
    for row in results:
        print(*row)


def pretty_output(results: List[List[str]]) -> None:
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results: List[List[str]], cli_args) -> None:
    results_dir = Path.cwd() / "results"
    results_dir.mkdir(exist_ok=True)

    mode = cli_args.mode
    now = datetime.now().strftime(DATETIME_FORMAT)
    file_name = f"{mode}_{now}.csv"
    file_path = results_dir / file_name

    with file_path.open(mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, dialect="unix", delimiter=";")
        writer.writerows(results)

    logging.info(f"Results saved to file: {file_path}")
