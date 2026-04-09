import pyjson5
import csv

def makeBoolean(value) -> bool:
	if value is None:
		return False
	elif isinstance(value, int):
		return False if value == 0 else True
	elif isinstance(value, str):
		v = value.lower()
		if v == "true":
			return True
		elif v == "false":
			return False
		elif v == "0":
			return False
		else:
			return True


def parse_schema_json(file_path) -> dict:
	print("json read")
	with open(file_path, "r", encoding="utf-8") as file:
		# Parse file content into a Python dictionary or list
		data = pyjson5.load(file)
		return data["fields"]


def parse_schema_csv(file_path):
	print("csv read")
	with open(file_path, mode="r", newline="", encoding="utf-8") as file:
		# Parse file content into a Python dictionary or list
		reader = csv.reader(file, delimiter=' ')
		items: list = []
		for row in reader:
			item = {"name": row[0], "type": row[1], "nullable": makeBoolean(row[2]), "start": int(row[4])}
			items.append(item)

		return items

def wip():
	print(parse_schema_json("sample.json"))
	print(parse_schema_csv("sample.csv"))


wip()
