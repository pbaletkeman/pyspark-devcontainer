"""
Data Generators Module
----------------------
Generates CSV files with random or schema-driven data for testing and development.

Classes:
    CreateData: Main class for generating data and writing to CSV files.

Usage:
    from data_generators import CreateData
    data = CreateData()
    data.load()
"""

import csv
from collections import defaultdict
from datetime import datetime, timedelta
import random
from typing import Iterator
import uuid

from faker import Faker, config

from schema_parser import Parser
from config import load_config
from util import Util


class CreateData:
    """
    Main class for generating data rows and writing them to a CSV file based on a schema.

    Loads configuration and schema, generates random data according to field types,
    and writes to CSV file in specified mode (overwrite or append).

    Attributes:
        config (dict): Configuration dictionary from load_config().
        auto_increment (int): Counter for auto-increment type fields.
    """

    def __init__(self):
        """
        Initialize CreateData with configuration and auto-increment counter.
        """
        self.config = load_config()
        self.autos = defaultdict(int)

    def create_file(self, schema: list):
        """
        Create a CSV file with data rows based on the provided schema.

        Writes the header row (unless in append mode), then generates and writes
        the specified number of data rows from the schema.

        Args:
            schema (list): List of field definition dictionaries from Parser.
        """
        COUNTER_ROW = 50

        first_row: dict = next(self.create_item(schema))
        fields_names: list = list(first_row.keys())
        mode: str = "w"

        if self.config["mode"].lower() in ("a", "append"):
            mode = "a"

        print(f"{datetime.now()} - Starting data generation with config: {self.config}")
        print(f"{datetime.now()} - Creating file {self.config['output']} with mode {mode} and fields {fields_names}")

        with open(self.config["output"], mode=mode, newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields_names, quoting=csv.QUOTE_ALL)

            if mode == "w":
                writer.writeheader()

            writer.writerow(first_row)

            for i in range(self.config["default_rows"] - 1):
                if i % COUNTER_ROW == 0:
                    print(f"{datetime.now()} - Creating row {i + 1}")
                writer.writerows(self.create_item(schema))

        print(f"{datetime.now()} - Finished data generation")

    def create_item(self, schema: list) -> Iterator[dict]:
        """
        Generate a single data row as a dictionary based on the schema.

        Iterates through schema fields, generates appropriate data for each type,
        and yields a complete row dictionary.

        Args:
            schema (list): List of field definition dictionaries.

        Yields:
            dict: A dictionary representing a single data row with field names as keys.
        """

        single_line: dict = {}
        null_threshold: float = self.config.get("default_null_percentage", 10.0) / 100.0

        if self.config.get("seed"):
            random.seed(self.config["seed"])
        for row in schema:
            data = ""
            field_type = row.get("type", "").lower().strip()
            nulls: float = random.random()

            if field_type == "stringtype":
                data = self.handle_stringtype(row)
            elif field_type == "randomtexttype":
                data = self.handle_randomtexttype(row)
            elif field_type == "integertype":
                data = self.handle_integertype(row)
            elif field_type == "doubletype":
                data = self.handle_doubletype(row)
            elif field_type == "floattype":
                data = self.handle_floattype(row)
            elif field_type == "booleantype":
                data = self.handle_booleantype(row)
            elif field_type == "datetype":
                data = self.handle_datetype(row)
            elif field_type == "timestamptype":
                data = self.handle_timestamptype(row)
            elif field_type == "uuidtype":
                data = self.handle_uuidtype(row)
            elif field_type == "valuetype":
                data = self.handle_valuetype(row)
            elif field_type == "autoincrementtype":
                data = self.handle_autoincrementtype(row)
            if row["nullable"] and nulls <= null_threshold and field_type != "autoincrementtype":
                single_line[row["name"]] = ""
            else:
                single_line[row["name"]] = str(data).strip('"')

        yield single_line

    def handle_randomtexttype(self, row: dict) -> str:
        LETTERS_NUMBER = "abcdefghijklmnopqrstuvwxyz0123456789-+*/+=-|;:<>,.ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        retval: str = ""
        l = row.get("length",10)
        for i in range(int(l)):
            retval = str(retval) + LETTERS_NUMBER[random.randint(0,len(LETTERS_NUMBER))-1]

        return retval

    def handle_valuetype(self, row: dict) -> str:
        """
        Handle fields of type 'valuetype', randomly selecting from provided values.

        Parses pipe-separated values and returns a random selection.
        Respects seed configuration for reproducibility.

        Args:
            row (dict): Schema field definition with 'values' key containing pipe-separated options.

        Returns:
            str: Selected value as string, or empty string if no values provided.
        """
        if self.config.get("seed"):
            random.seed(self.config["seed"])

        if row.get("values"):
            values = row["values"].split("|")
            v = [x.strip().strip('"').strip('"') for x in values]
            max_index = len(v) - 1
            return str(v[random.randint(0, max_index)])
        return ""

    def handle_stringtype(self, row: dict) -> str:
        """
        Handle fields of type 'stringtype', generating random names using Faker.

        Generates realistic random names. Truncates to f_length if specified.
        Respects seed configuration for reproducibility.

        Args:
            row (dict): Schema field definition with optional 'length' key.

        Returns:
            str: Generated random name.
        """
        fake = Faker()
        if self.config.get("seed"):
            Faker.seed(self.config["seed"])

        name = fake.name()
        if row.get("length"):
            return name[: int(row["length"])]
        return name

    def handle_integertype(self, row: dict) -> str:
        """
        Handle fields of type 'integertype', generating random integers.

        Generates random integers within configured range.
        Respects seed configuration for reproducibility.

        Args:
            row (dict): Schema field definition.

        Returns:
            str: Generated integer as string.
        """
        if self.config.get("seed"):
            random.seed(self.config["seed"])

        int_range = self.config.get("integer_range", [0, 10])
        return str(random.randint(int(int_range[0]), int(int_range[-1])))

    def handle_doubletype(self, row: dict) -> str:
        """
        Handle fields of type 'doubletype', generating random floats.

        Generates random floats within configured range with 5 decimal precision.
        Respects seed configuration for reproducibility.

        Args:
            row (dict): Schema field definition.

        Returns:
            str: Generated float as string with 5 decimal places.
        """
        if self.config.get("seed"):
            random.seed(self.config["seed"])

        float_range = self.config.get("float_range", [0, 10])
        return f"{random.uniform(float(float_range[0]), float(float_range[-1])):.5f}"

    def handle_floattype(self, row: dict) -> str:
        """
        Handle fields of type 'floattype', generating random floats.

        Delegates to handle_doubletype as both types generate floats.

        Args:
            row (dict): Schema field definition.

        Returns:
            str: Generated float as string.
        """
        return self.handle_doubletype(row)

    def handle_booleantype(self, row: dict) -> str:
        """
        Handle fields of type 'booleantype', generating random boolean values.

        Generates random 0 or 1, then converts to boolean string.
        Respects seed configuration for reproducibility.

        Args:
            row (dict): Schema field definition.

        Returns:
            str: Generated boolean as string ("True" or "False").
        """
        if self.config.get("seed"):
            random.seed(self.config["seed"])

        return str(Util.make_boolean(random.randint(0, 1)))

    def handle_timestamptype(self, row: dict) -> str:
        """
        Handle fields of type 'timestamptype', generating random timestamps.

        Generates random timestamps within configured date/timestamp range.
        Returns formatted as "YYYY-MM-DD HH:MM:SS.ffffff".
        Respects seed configuration for reproducibility.

        Args:
            row (dict): Schema field definition.

        Returns:
            str: Generated timestamp as formatted string.
        """
        if self.config.get("seed"):
            random.seed(self.config["seed"])

        date_range = self.config.get("date_range", None)

        if not date_range:
            start = datetime.today()
            end = datetime.today() + timedelta(weeks=52)
        elif isinstance(date_range, (list, tuple)):
            start = Util.parse_date(date_range[0])
            end = Util.parse_date(date_range[-1])
        else:
            start = Util.parse_date(date_range)
            end = start + timedelta(weeks=52)

        return str(Util.get_random_date(start, end).strftime("%Y-%m-%d %H:%M:%S.%f"))

    def handle_datetype(self, row: dict) -> str:
        """
        Handle fields of type 'datetype', generating random dates.

        Delegates to handle_timestamptype and extracts date portion only.
        Returns formatted as "YYYY-MM-DD".

        Args:
            row (dict): Schema field definition.

        Returns:
            str: Generated date as formatted string.
        """
        return str(self.handle_timestamptype(row).split(" ")[0])

    def handle_uuidtype(self, row: dict) -> str:
        """
        Handle fields of type 'uuidtype', generating UUIDs.

        Generates a unique UUID version 1 for each field.

        Args:
            row (dict): Schema field definition.

        Returns:
            str: Generated UUID as string.
        """
        return str(uuid.uuid1())

    def handle_autoincrementtype(self, row: dict) -> str:
        """
        Handle fields of type 'autoincrementtype', generating incrementing integers.

        Maintains internal counter starting from f_start value.
        Increments counter and returns new value for each row.

        Args:
            row (dict): Schema field definition with optional 'start' value.

        Returns:
            str: Generated auto-increment value as string.
        """
        start_value = int(row.get("start", self.autos[row["name"]]))
        self.autos[row["name"]] = start_value + 1
        row["start"] = self.autos[row["name"]]
        return str(self.autos[row["name"]])

    def load(self) -> None:
        """
        Load schema from configuration and generate the output file.

        Entry point for data generation. Parses schema file specified in config,
        then calls create_file to generate CSV.
        """
        schema = Parser.parse_schema(file_path=self.config["schema"])
        self.create_file(schema)


def wip():
    """
    Entry point for running data generation as a script.
    Creates a CreateData instance and calls load() to generate data.
    """
    data: CreateData = CreateData()
    data.load()


if __name__ == "__main__":
    wip()
