import pyjson5
import csv
from util import Util


class Parser():

	@classmethod
	def parse_schema(cls, file_path) -> dict:
		if str(file_path.lower()).endswith(".json"):
			return Parser.parse_schema_json(file_path)
		else:
			return Parser.parse_schema_csv(file_path)

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
				item = {"name": row["name"],
					"type": row["type"],
					"nullable": Util.make_boolean(row["nullable"]),
					"start": int(row["start"]),
					"length": int(row["length"]),
					"values": row["values"]
				}
				items.append(item)

			return items

# def wip():
# 	print(parse_schema_json("sample.json"))
# 	print(parse_schema_csv("sample.csv"))


# wip()
