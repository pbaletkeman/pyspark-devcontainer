import random

from faker import Faker

from schema_parser import (parse_schema_json, parse_schema_csv, makeBoolean)
from config import load_config


class CreateData():

	def __init__(self):
		self.config = load_config()


	def create_lines(self, schema: list[dict]) -> str:
		for row in schema:
			data: str = ""
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
				# case "datetype":
				# 	data = self.handle_datetype(row)
				# case "timestamptype":
				# 	data = self.handle_timestamptype(row)
				# case "uuidtype":
				# 	data = self.handle_uuidtype(row)
				# case "autoincrementtype":
				# 	data = self.handle_autoincrementtype(row)

			print(data)

	def handle_randomtexttype(self, row: dict) -> str:
		fake = Faker()
		if self.config["seed"]:
			Faker.seed(self.config["seed"])
		return fake.text()[:row["length"]]

	def handle_stringtype(self, row: dict) -> str:
		fake = Faker()
		if self.config["seed"]:
			Faker.seed(self.config["seed"])
		return fake.name()[:row["length"]]

	def handle_integertype(self, row: dict) -> int:
		if self.config["seed"]:
			random.seed = self.config["seed"]
		return random.randint(int(row["min"]), int(row["max"]))

	def handle_doubletype(self, row: dict) -> float:
		if self.config["seed"]:
			random.seed = self.config["seed"]
		return random.uniform(int(row["min"]), int(row["max"]))

	def handle_floattype(self, row: dict) -> str:
		return self.handle_doubletype(row)

	def handle_booleantype(self, row: dict) -> str:
		if self.config["seed"]:
			random.seed = self.config["seed"]
		return makeBoolean(random.randint(0, 1))

	def handle_datetype(self, row: dict) -> str:
		pass

	def handle_timestamptype(self, row: dict) -> str:
		pass

	def handle_uuidtype(self, row: dict) -> str:
		pass

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
