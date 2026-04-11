"""
Configuration Loader Module
---------------------------
Handles loading and parsing of configuration files and command-line arguments
for data generation. Combines JSON5 config files with CLI arguments.

Functions:
    load_config_file(file_path): Load JSON5 configuration file.
    load_config(): Parse CLI arguments and merge with config file or defaults.
"""

import argparse
from datetime import date
import datetime
import pyjson5


def load_config_file(file_path: str) -> dict:
    """
    Load a configuration file in JSON5 format.

    Args:
        file_path (str): Path to the config file. If None, attempts to load from 'config.json'
                        in current directory.

    Returns:
        dict: Parsed configuration dictionary, or None if file not found.
    """
    import os

    # If no path provided, try to auto-detect config.json
    if not file_path:
        if os.path.exists("config.json"):
            file_path = "config.json"
        else:
            return None

    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            data = pyjson5.load(file)
            return data
    return None


def load_config() -> dict:
    """
    Parse command-line arguments and merge with config file or defaults.

    Returns:
        dict: Final configuration dictionary for data generation.
    """
    parser = argparse.ArgumentParser(description="Generate CSV files with random or schema-driven data.")
    parser.add_argument("schema", type=str, help="File containing schema definition [*.json|*.csv]")
    parser.add_argument("output", type=str, help="Resulting output file path")
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        help="Write mode for resulting file [append|overwrite]",
        choices=["append", "a", "overwrite", "o"],
        default="overwrite",
    )
    parser.add_argument("--config", type=str, help="Config file path (JSON5 format)")
    parser.add_argument("-r", "--rows", type=int, help="Number of rows to create")
    parser.add_argument("-np", "--null_percentage", type=int, help="Percentage of null values")
    parser.add_argument(
        "-nfo",
        "--nullable_field_overrides",
        nargs="+",
        type=str,
        help="Fields that can't be null (space-separated)",
    )
    parser.add_argument("-s", "--seed", type=int, help="Random seed value for reproducible results")
    parser.add_argument("-ir", "--integer_range", type=int, nargs=2, help="Lower and upper int bounds")
    parser.add_argument("-fr", "--float_range", type=int, nargs=2, help="Lower and upper float bounds")
    parser.add_argument("-dr", "--date_range", type=date, nargs=2, help="Lower and upper date bounds")
    parser.add_argument(
        "-tr",
        "--timestamp_range",
        type=datetime.datetime,
        nargs=2,
        help="Lower and upper datetime bounds",
    )

    args = parser.parse_args()
    config = load_config_file(args.config)

    if config:
        config["schema"] = args.schema
        config["output"] = args.output
        config["mode"] = args.mode
        config["default_rows"] = args.rows or config.get("default_rows", 10)
        config["default_null_percentage"] = args.null_percentage or config.get("default_null_percentage", 10.0)
        config["seed"] = args.seed or config.get("seed")
        config["integer_range"] = args.integer_range or config.get("integer_range", [0, 10])
        config["float_range"] = args.float_range or config.get("float_range", [0.0, 10.0])
        config["date_range"] = args.date_range or config.get("date_range", datetime.date.today())
        config["timestamp_range"] = args.timestamp_range or config.get("timestamp_range", datetime.date.today())
    else:
        config = {
            "output": args.output,
            "mode": args.mode,
            "schema": args.schema,
            "default_rows": args.rows or 10,
            "default_null_percentage": args.null_percentage or 10.0,
            "seed": args.seed,
            "integer_range": args.integer_range or [10, 1000],
            "float_range": args.float_range or [10.0, 1000.0],
            "date_range": args.date_range or datetime.date.today(),
            "timestamp_range": args.timestamp_range or datetime.date.today(),
        }

    return config
