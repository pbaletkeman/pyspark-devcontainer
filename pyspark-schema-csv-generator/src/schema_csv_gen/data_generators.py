import csv
from datetime import datetime, timedelta
import random
from typing import Iterator
import uuid

from faker import Faker

from schema_parser import Parser
from config import load_config
from util import Util

class CreateData():

	def __init__(self):
		self.config = load_config()
		self.auto_increment = 0


	def create_file(self, schema: list[dict]):

		first_row: dict = next(self.create_item(schema))
		fields_names: list = list(first_row.keys())

		with open("sample-new.csv", "w", newline="", encoding="utf-8") as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=fields_names)

			writer.writerow(first_row)
			for i in range(self.config["default_rows"]):
				writer.writerows(self.create_item(schema))


	def create_item(self, schema: list[dict]) -> Iterator[dict]:
		single_line: dict = {}
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
				case "autoincrementtype":
					data = self.handle_autoincrementtype(row)
			single_line = single_line | {row["name"]: data}
		yield single_line


	def handle_valuetype(self, row: dict) -> str:
		if self.config["seed"]:
			random.seed = self.config["seed"]
		if row["values"]:
			values = row["values"].split("|")
			v = [x.strip() for x in values]
			max = len(v)-1
			return str(v[random.randint(0,max)])
		return ""


	def handle_randomtexttype(self, row: dict) -> str:
		fake = Faker()
		if self.config["seed"]:
			Faker.seed(self.config["seed"])
		if row["length"]:
			return fake.text()[:int(row["length"])]
		return fake.text()


	def handle_stringtype(self, row: dict) -> str:
		fake = Faker()
		if self.config["seed"]:
			Faker.seed(self.config["seed"])
		if row["length"]:
			return fake.name()[:int(row["length"])]
		return fake.name()


	def handle_integertype(self, row: dict) -> int:
		if self.config["seed"]:
			random.seed = self.config["seed"]
		int_range = self.config.get("integer_range", [0, 10])

		return str(random.randint(int(int_range[0]), int(int_range[-1])))


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
		return str(Util.make_boolean(random.randint(0, 1)))


	def handle_timestamptype(self, row: dict) -> str:
		if self.config["seed"]:
			random.seed = self.config["seed"]
		date_range = self.config.get("date_range", None)
		if not date_range:
			start = datetime.today()
			end = datetime.today() + timedelta(weeks=52)
		elif isinstance(date_range, (list, tuple)):
			start = Util.parse_date(date_range[0])
			end = Util.parse_date(date_range[-1])
		else:
			# If it's a single date/datetime object, use it as start, and add 1 year for end
			start = Util.parse_date(date_range)
			end = start + timedelta(weeks=52)
		return str(Util.get_random_date(start, end).strftime("%Y-%m-%d %H:%M:%S.%f"))


	def handle_datetype (self, row: dict) -> str:
		return str(self.handle_timestamptype(row).split(" ")[0])


	def handle_uuidtype(self, row: dict) -> str:
		return str(uuid.uuid1())


	def handle_autoincrementtype(self, row: dict) -> str:
		self.auto_increment = int(row.get("start", self.auto_increment))
		self.auto_increment += 1
		row["start"] = self.auto_increment
		return str(self.auto_increment)


	def load(self) -> None:
		self.create_file (Parser.parse_schema(file_path=self.config["schema"]))


def wip():
	data: CreateData = CreateData()
	data.load()

wip()
