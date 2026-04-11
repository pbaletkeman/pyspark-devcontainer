import pyjson5
import csv
from util import Util


class Parser():

	@classmethod
	def parse_schema(cls, file_path) -> dict:
		retval: dict = {}
		if str(file_path.lower()).endswith(".json"):
			retval = Parser.parse_schema_json(file_path)
		else:
			retval = Parser.parse_schema_csv(file_path)

		if Parser.has_duplicate_auto(retval):
			raise Exception("duplicate field auto increment")

		if Parser.has_duplicate_names(retval):
			raise Exception("duplicate field in schema")

		return retval

	@classmethod
	def parse_schema_json(cls, file_path: str) -> dict:
		with open(file_path, "r", encoding="utf-8") as file:
			# Parse file content into a Python dictionary or list
			data = pyjson5.load(file)
			return data["fields"]

	@classmethod
	def parse_schema_csv(cls, file_path: str):
		with open(file_path, mode="r", newline="", encoding="utf-8") as file:
			# Parse file content into a Python dictionary or list
			reader = csv.DictReader(file, delimiter=',',)
			items: list = []
			for row in reader:
				# print(row)
				item = {"name": row["f_name"],
					"type": row["f_type"],
					"nullable": Util.make_boolean(row["f_nullable"]),
					"start": row.get("f_start", 0),
					"length": row.get("f_length", 0),
					"values": row.get("f_values", "")
				}
				items.append(item)

			return items

	@classmethod
	def has_duplicate_auto(cls, records: list[dict]) -> bool:
		auto_found = False
		for record in records:
			if record.get("type").lower() == "autoincrementtype":
				if auto_found:
					return True
				else:
					auto_found = True
		return False

	@classmethod
	def has_duplicate_names(cls, records: list[dict]) -> bool:
		key = "name"
		names = set()
		for record in records:
			name = record.get(key)
			if name in names:
				return True
			names.add(name)
		return False

# def wip():
# 	print(parse_schema_json("sample.json"))
# 	print(parse_schema_csv("sample.csv"))


# wip()
