from datetime import date
import datetime
from email.policy import default

import pyjson5
import argparse


def load_config(file_path: str) -> dict:
	print("json read")
	with open(file_path, "r", encoding="utf-8") as file:
		# Parse file content into a Python dictionary or list
		data = pyjson5.load(file)
		return data

def load_args(in_config: dict | None) -> dict:
	parser = argparse.ArgumentParser()
	parser.add_argument("--rows", default=100, type=int, help="number of rows to create")
	parser.add_argument("--null_percentage", default=10, type=int, help="percentage of null values")
	parser.add_argument("--nullable_field_overrides", type=str, help="fields that can't be null")
	parser.add_argument("--seed", type=int, help="random seed value for reproduceable results")
	parser.add_argument("--integer_range", default = [-1000, 1000], type=int, nargs="+", help="lower and upper int bounds")
	parser.add_argument("--float_range", default = [-1000.0, 1000.0], type=int, nargs="+", help="lower and upper float bounds")
	parser.add_argument("--date_range", default = ["2024-04-09", "2027-04-09"], type=date, nargs="+", help="lower and upper date bounds")
	parser.add_argument("--timestamp_range", default = ["2024-04-09T00:00:00", "2027-04-09T23:59:59"], type=datetime.datetime, nargs="+", help="lower and update datetime bounds")
	args = parser.parse_args()
	config = in_config.copy()
	if config:
		config["default_rows"] = args.rows if args.rows else config["rows"]
		config["default_null_percentage"] = args.null_percentage if args.null_percentage else config["default_null_percentage"]
		config["nullable_field_overrides"] = args.nullable_field_overrides if args.nullable_field_overrides  else config["nullable_field_overrides"]
		config["seed"] = args.seed if args.seed else config["seed"]
		config["integer_range"] = args.integer_range if args.integer_range else config["integer_range"]
		config["float_range"] = args.float_range if args.float_range else config["float_range"]
		config["date_range"] = args.date_range if args.date_range else config["date_range"]
		config["timestamp_range"] = args.timestamp_range if args.timestamp_range else config["timestamp_range"]
	else:
		config["default_rows"] = args.rows
		config["default_null_percentage"] = args.null_percentage
		config["nullable_field_overrides"] = args.nullable_field_overrides
		config["seed"] = args.seed
		config["integer_range"] = args.integer_range
		config["float_range"] = args.float_range
		config["date_range"] = args.date_range
		config["timestamp_range"] = args.timestamp_range

	return config



def wip():
	config = load_config("config.json")
	print(load_args(config))

wip()
