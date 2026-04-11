"""
Utility Functions Module
------------------------
Provides helper functions for boolean conversion, random date generation,
and date parsing. Used by data generation and parsing modules.

Classes:
    Util: Static utility methods for data generation.
"""
from datetime import datetime, timedelta
import random


class Util():
    """
    Utility class with static methods for data generation and parsing.

    Provides common functionality for boolean conversion, random date
    generation, and flexible date parsing.
    """

    @classmethod
    def make_boolean(cls, value) -> bool:
        """
        Convert a value to boolean, handling int and str representations.

        Conversion rules:
            - None: False
            - int: False if 0, True otherwise
            - str "true": True (case-insensitive)
            - str "false": False (case-insensitive)
            - str "0": False
            - any other str: True

        Args:
            value: Value to convert (bool, int, str, or None).

        Returns:
            bool: Converted boolean value.
        """
        if value is None:
            return False
        elif isinstance(value, bool):
            return value
        elif isinstance(value, int):
            return False if value == 0 else True
        elif isinstance(value, str):
            v = value.lower().strip()
            if v == "true":
                return True
            elif v == "false":
                return False
            elif v == "0":
                return False
            else:
                return True
        return False

    @classmethod
    def get_random_date(cls, start: datetime, end: datetime) -> datetime:
        """
        Generate a random datetime between two datetime objects.

        Generates a uniform random datetime including both date and time
        components between the two bounds.

        Args:
            start (datetime): Start datetime (inclusive).
            end (datetime): End datetime (inclusive).

        Returns:
            datetime: Random datetime between start and end.
        """
        delta = end - start
        int_delta = int(delta.total_seconds())
        random_second = random.randrange(int_delta)
        return start + timedelta(seconds=random_second)

    @classmethod
    def parse_date(cls, date_val) -> datetime:
        """
        Parse a date value (str, date, or datetime) into a datetime object.

        Supports multiple input formats:
            - datetime objects: returned as-is
            - date objects: converted to datetime at midnight (00:00:00)
            - str in format "YYYY-MM-DD HH:MM:SS": parsed directly
            - str in format "YYYY-MM-DD": parsed as date at midnight

        Args:
            date_val: Date value to parse (str, date, datetime, or object with year/month/day).

        Returns:
            datetime: Parsed datetime object.

        Raises:
            ValueError: If the date format is not recognized.
        """
        if isinstance(date_val, datetime):
            return date_val

        if hasattr(date_val, "year") and hasattr(date_val, "month") and hasattr(date_val, "day"):
            return datetime(date_val.year, date_val.month, date_val.day)

        if isinstance(date_val, str):
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
                try:
                    return datetime.strptime(date_val, fmt)
                except ValueError:
                    continue

        raise ValueError(f"Date '{date_val}' is not in a recognized format or type.")
