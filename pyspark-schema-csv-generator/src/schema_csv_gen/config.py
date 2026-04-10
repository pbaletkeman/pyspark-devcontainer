from datetime import date
import datetime
from email.policy import default

import pyjson5
import argparse


def load_config_file(file_path: str) -> dict:
	if file_path:
		with open(file_path, "r", encoding="utf-8") as file:
			# Parse file content into a Python dictionary or list
			data = pyjson5.load(file)
			return data

def load_config() -> dict:
	parser = argparse.ArgumentParser()
	parser.add_argument("schema", type=str,  help="config file path.json")
	parser.add_argument("--config", type=str,  help="config file path.json")
	parser.add_argument("-r", "--rows", default=100, type=int, help="number of rows to create")
	parser.add_argument("-np", "--null_percentage", default=10, type=int, help="percentage of null values")
	parser.add_argument("-nfo", "--nullable_field_overrides", nargs="+", type=str, help="fields that can't be null")
	parser.add_argument("-s", "--seed", type=int, help="random seed value for reproduceable results")
	parser.add_argument("-ir", "--integer_range", default = [-1000, 1000], type=int, nargs=2, help="lower and upper int bounds")
	parser.add_argument("-fr", "--float_range", default = [-1000.0, 1000.0], type=int, nargs=2, help="lower and upper float bounds")
	parser.add_argument("-dr", "--date_range", default = ["2024-04-09", "2027-04-09"], type=date, nargs=2, help="lower and upper date bounds")
	parser.add_argument("-tr", "--timestamp_range", default = ["2024-04-09T00:00:00", "2027-04-09T23:59:59"], type=datetime.datetime, nargs=2, help="lower and update datetime bounds")
	args = parser.parse_args()
	config = load_config_file(args.config)
	if config:
		config["schema"] = args.schema
		config["default_rows"] = args.rows if args.rows else config["rows"]
		config["default_null_percentage"] = args.null_percentage if args.null_percentage else config["default_null_percentage"]
		if args.nullable_field_overrides:
			config["nullable_field_overrides"] = [f.strip() for f in args.nullable_field_overrides.split(",")]
		else:
			config["nullable_field_overrides"] = config.get("nullable_field_overrides", [])
		if args.seed:
			config["seed"] = args.seed
		config["integer_range"] = args.integer_range if args.integer_range else config["integer_range"]
		config["float_range"] = args.float_range if args.float_range else config["float_range"]
		config["date_range"] = args.date_range if args.date_range else config["date_range"]
		config["timestamp_range"] = args.timestamp_range if args.timestamp_range else config["timestamp_range"]
	else:
		config = {
			"schema": args.schema,
			"default_rows": args.rows,
			"default_null_percentage" : args.null_percentage,
			"nullable_field_overrides": args.nullable_field_overrides,
			"seed": args.seed,
			"integer_range": args.integer_range,
			"float_range": args.float_range,
			"date_range": args.date_range,
			"timestamp_range": args.timestamp_range}
	return config
