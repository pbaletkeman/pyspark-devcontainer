import random
from datetime import datetime, timedelta
import uuid

from faker import Faker

from schema_parser import (parse_schema_json, parse_schema_csv, makeBoolean)
from config import load_config


def get_random_date(start, end):
    """Generates a random datetime between two datetime objects."""
    delta = end - start
    # Calculate total seconds to allow for random time as well as date
    int_delta = int(delta.total_seconds())
    random_second = random.randrange(int_delta * 1020304)
    return start + timedelta(microseconds=random_second)

def parse_date(date_val):
    if isinstance(date_val, datetime):
        return date_val
    # Add support for datetime.date
    if hasattr(date_val, "year") and hasattr(date_val, "month") and hasattr(date_val, "day"):
        # Convert date to datetime at midnight
        return datetime(date_val.year, date_val.month, date_val.day)
    if isinstance(date_val, str):
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(date_val, fmt)
            except ValueError:
                continue
    raise ValueError(f"Date '{date_val}' is not in a recognized format or type.")

class CreateData():

	def __init__(self):
		self.config = load_config()


	def create_lines(self, schema: list[dict]) -> str:
		single_line: dict = {}
		all_lines: list[str] = []
		data: str = ""
		for i in range(self.config["default_rows"]):
			for row in schema:
				data = ""
				match row["type"].lower():
					case "stringtype":
						data = self.handle_stringtype(row)
					case "randomtexttype":
						data = self.handle_randomtexttype(row)
					case "integertype":
						data = self.handle_integertype(row)
					case "doubletype":
						data = self.handle_doubletype(row)
					case "floattype":
						data = self.handle_floattype(row)
					case "booleantype":
						data = self.handle_booleantype(row)
					case "datetype":
						data = self.handle_datetype(row)
					case "timestamptype":
						data = self.handle_timestamptype(row)
					case "uuidtype":
						data = self.handle_uuidtype(row)
					case "valuetype":
						data = self.handle_valuetype(row)
					# case "autoincrementtype":
					# 	data = self.handle_autoincrementtype(row)
				single_line = single_line | {row["name"]: data}
				# all_lines.append(single_line)
			# print(single_line)

	def handle_valuetype(self, row: dict) -> str:
		if self.config["seed"]:
			random.seed = self.config["seed"]
		if row["values"]:
			values = row["values"].split("|")
			v = [x.strip() for x in values]
			max = len(v)-1
			return v[random.randint(0,max)]
		return ""

	def handle_randomtexttype(self, row: dict) -> str:
		fake = Faker()
		if self.config["seed"]:
			Faker.seed(self.config["seed"])
		if row["length"]:
			return fake.text()[:row["length"]]
		return fake.text()

	def handle_stringtype(self, row: dict) -> str:
		fake = Faker()
		if self.config["seed"]:
			Faker.seed(self.config["seed"])
		if row["length"]:
			return fake.name()[:row["length"]]
		return fake.name()

	def handle_integertype(self, row: dict) -> int:
		if self.config["seed"]:
			random.seed = self.config["seed"]
		int_range = self.config.get("integer_range", [0, 10])

		return random.randint(int(int_range[0]), int(int_range[-1]))

	def handle_doubletype(self, row: dict) -> float:
		if self.config["seed"]:
			random.seed = self.config["seed"]
		float_range = self.config.get("float_range", [0, 10])
		return f"{random.uniform(float(float_range[0]), float(float_range[-1])):.5f}"

	def handle_floattype(self, row: dict) -> str:
		return self.handle_doubletype(row)

	def handle_booleantype(self, row: dict) -> str:
		if self.config["seed"]:
			random.seed = self.config["seed"]
		return makeBoolean(random.randint(0, 1))

	def handle_timestamptype(self, row: dict) -> str:
		if self.config["seed"]:
			random.seed = self.config["seed"]
		date_range = self.config.get("date_range", None)
		if not date_range:
			start = datetime.today()
			end = datetime.today() + timedelta(weeks=52)
		elif isinstance(date_range, (list, tuple)):
			start = parse_date(date_range[0])
			end = parse_date(date_range[-1])
		else:
			# If it's a single date/datetime object, use it as start, and add 1 year for end
			start = parse_date(date_range)
			end = start + timedelta(weeks=52)
		return get_random_date(start, end).strftime("%Y-%m-%d %H:%M:%S.%f")

	def handle_datetype (self, row: dict) -> str:
		return self.handle_timestamptype(row).split(" ")[0]

	def handle_uuidtype(self, row: dict) -> str:
		return str(uuid.uuid1())

	def handle_autoincrementtype(self, row: dict) -> str:
		pass

	def load(self) -> None:

		if self.config["schema"].lower().endswith("json"):
			schema = parse_schema_json(self.config["schema"])
		else:
			schema = parse_schema_csv(self.config["schema"])
		self.create_lines(schema)


def wip():
	data: CreateData = CreateData()
	data.load()

wip()
