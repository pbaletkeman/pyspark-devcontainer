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
	parser.add_argument("-r", "--rows", type=int, help="number of rows to create")
	parser.add_argument("-np", "--null_percentage", type=int, help="percentage of null values")
	parser.add_argument("-nfo", "--nullable_field_overrides", nargs="+", type=str, help="fields that can't be null")
	parser.add_argument("-s", "--seed", type=int, help="random seed value for reproduceable results")
	parser.add_argument("-ir", "--integer_range", type=int, nargs=2, help="lower and upper int bounds")
	parser.add_argument("-fr", "--float_range", type=int, nargs=2, help="lower and upper float bounds")
	parser.add_argument("-dr", "--date_range", type=date, nargs=2, help="lower and upper date bounds")
	parser.add_argument("-tr", "--timestamp_range", default = ["2024-04-09T00:00:00", "2027-04-09T23:59:59"], type=datetime.datetime, nargs=2, help="lower and update datetime bounds")
	args = parser.parse_args()
	config = load_config_file(args.config)
	if config:
		config["schema"] = args.schema
		if args.nullable_field_overrides:
			config["default_rows"] = args.rows
		else:
			config["default_rows"] = 2
		if args.null_percentage:
			config["default_null_percentage"] = args.null_percentage
		else:
			config["default_null_percentage"] = 5
		if args.nullable_field_overrides:
			config["nullable_field_overrides"] = [f.strip() for f in args.nullable_field_overrides.split(",")]
		else:
			config["nullable_field_overrides"] = config.get("nullable_field_overrides", [])
		if args.seed:
			config["seed"] = args.seed
		if args.integer_range:
			config["integer_range"] = args.integer_range
		else:
			config["integer_range"] = [1,10]
		if args.float_range:
			config["float_range"] = args.float_range
		else:
			config["float_range"] = [-10,10]
		if args.date_range:
			config["date_range"] = args.date_range
		else:
			config["date_range"] = datetime.date.today()
		if args.timestamp_range:
			config["timestamp_range"] = args.timestamp_range
		else:
			config["timestamp_range"] = datetime.date.today()
	else:
		config = {
			"schema": args.schema,
			"default_rows": args.rows or 10,
			"default_null_percentage" : args.null_percentage or 5,
			"nullable_field_overrides": args.nullable_field_overrides,
			"seed": args.seed,
			"integer_range": args.integer_range or [0,10],
			"float_range": args.float_range or [-10,10],
			"date_range": args.date_range or datetime.date.today(),
			"timestamp_range": args.timestamp_range or datetime.date.today()}
	return config
