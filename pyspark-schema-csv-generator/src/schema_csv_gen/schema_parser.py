"""
Schema Parser Module
--------------------
Parses schema definitions from JSON or CSV files for data generation.

Classes:
    Parser: Main class for parsing and validating schema files.
"""

import pyjson5
import csv
from util import Util


class Parser:
    """
    Class for parsing schema files and validating schema definitions.

    Supports both JSON5 and CSV schema formats. Validates for duplicate
    field names and auto-increment fields.
    """

    @classmethod
    def parse_schema(cls, file_path) -> list:
        """
        Parse a schema file (JSON or CSV) and return a list of field definitions.

        Automatically detects file format based on extension (.json or .csv).
        Validates schema for duplicate field names and auto-increment fields.

        Args:
            file_path (str): Path to the schema file.

        Returns:
            list: List of field definition dictionaries.

        Raises:
            Exception: If duplicate auto-increment or field names are found.
        """
        retval: list = []
        if str(file_path).lower().endswith(".json"):
            retval = cls.parse_schema_json(file_path)
        else:
            retval = cls.parse_schema_csv(file_path)

        if cls.has_duplicate_auto(retval):
            raise Exception("duplicate field auto increment")

        if cls.has_duplicate_names(retval):
            raise Exception("duplicate field in schema")

        return retval

    @classmethod
    def parse_schema_json(cls, file_path: str) -> list:
        """
        Parse a JSON5 schema file and return field definitions.

        Expected JSON structure:
            {"fields": [{"name": "...", "type": "...", ...}, ...]}

        Args:
            file_path (str): Path to the JSON schema file.

        Returns:
            list: List of field definition dictionaries.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            data = pyjson5.load(file)
            return data.get("fields", [])

    @classmethod
    def parse_schema_csv(cls, file_path: str) -> list:
        """
        Parse a CSV schema file and return field definitions.

        Expected CSV columns: f_name, f_type, f_nullable, f_start, f_length, f_values

        Args:
            file_path (str): Path to the CSV schema file.

        Returns:
            list: List of field definition dictionaries.
        """
        with open(file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=",")
            items: list = []
            for row in reader:
                item = {
                    "name": row["f_name"],
                    "type": row["f_type"],
                    "nullable": Util.make_boolean(row["f_nullable"]),
                    "start": row.get("f_start", 0),
                    "length": row.get("f_length", 0),
                    "values": row.get("f_values", ""),
                }
                items.append(item)
            return items

    @classmethod
    def has_duplicate_auto(cls, records: list) -> bool:
        """
        Check for duplicate auto-increment fields in schema.

        Only one field can have type 'autoincrementtype'.

        Args:
            records (list): List of field definition dictionaries.

        Returns:
            bool: True if duplicate auto-increment found, False otherwise.
        """
        auto_found = False
        for record in records:
            if record.get("type", "").lower() == "autoincrementtype":
                if auto_found:
                    return True
                auto_found = True
        return False

    @classmethod
    def has_duplicate_names(cls, records: list) -> bool:
        """
        Check for duplicate field names in schema.

        Field names must be unique within a schema.

        Args:
            records (list): List of field definition dictionaries.

        Returns:
            bool: True if duplicate names found, False otherwise.
        """
        key = "name"
        names = set()
        for record in records:
            name = record.get(key)
            if name in names:
                return True
            names.add(name)
        return False
