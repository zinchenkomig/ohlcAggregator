import collections.abc
import csv
from decimal import Decimal

from .time_utils import parse_timestamp


def csv_reader(filename: str) -> collections.abc.Iterator[(int, Decimal)]:
    with open(filename, newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip csv header
        for ts_str, price_str in reader:
            yield parse_timestamp(ts_str), Decimal(price_str)


def str_reader(data_str: str) -> collections.abc.Iterator[(int, Decimal)]:
    return map(lambda row: (parse_timestamp(row.strip().split(',')[0]),
                            Decimal(row.strip().split(',')[1])), data_str.strip().split('\n'))
