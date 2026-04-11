# Schema CSV Generator

A Python tool for generating synthetic CSV data using schema-driven definitions. Supports both CSV and JSON schema formats, flexible field types, null value control, and reproducible random data generation for testing and development.

- [Schema CSV Generator](#schema-csv-generator)
  - [Quick Start](#quick-start)
  - [Project Structure](#project-structure)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
  - [Usage](#usage)
    - [Command Line](#command-line)
      - [Required Arguments](#required-arguments)
      - [Options](#options)
      - [Examples](#examples)
    - [As a Python Module](#as-a-python-module)
  - [Configuration](#configuration)
    - [config.json](#configjson)
      - [Example config.json](#example-configjson)
      - [Configuration Fields](#configuration-fields)
  - [Schema Format](#schema-format)
    - [CSV Schema](#csv-schema)
    - [JSON Schema](#json-schema)
  - [Field Types](#field-types)
    - [Basic Types](#basic-types)
    - [Date \& Time Types](#date--time-types)
    - [Special Types](#special-types)
  - [Null Value Generation](#null-value-generation)
    - [How Nulls Work](#how-nulls-work)
    - [Example Scenario](#example-scenario)
    - [Key Points](#key-points)
  - [Code Modules](#code-modules)
    - [config.py](#configpy)
    - [schema\_parser.py](#schema_parserpy)
    - [data\_generators.py](#data_generatorspy)
    - [util.py](#utilpy)
  - [Examples](#examples-1)
    - [Example 1: Generate 20 Rows with 80% Nulls](#example-1-generate-20-rows-with-80-nulls)
    - [Example 2: Reproducible Data with Seed](#example-2-reproducible-data-with-seed)
    - [Example 3: Custom Integer and Float Ranges](#example-3-custom-integer-and-float-ranges)
  - [Troubleshooting](#troubleshooting)
  - [Code Quality](#code-quality)
  - [License](#license)
  - [Version History](#version-history)


---

## Quick Start

```bash
# Generate 10 rows using sample schema
python3 schema_csv_gen/data_generators.py schema_csv_gen/sample.csv schema_csv_gen/output.csv --rows 10 --mode overwrite

# Generate 100 rows with 80% null probability on nullable fields
python3 schema_csv_gen/data_generators.py schema_csv_gen/sample.csv schema_csv_gen/output.csv --rows 100 --null_percentage 80

# With custom config file
python3 schema_csv_gen/data_generators.py schema_csv_gen/sample.csv schema_csv_gen/output.csv --config custom_config.json
```

---

## Project Structure

```
.
├── schema_csv_gen/                 # Main source code directory
│   ├── config.json                 # Configuration file (auto-loaded by default)
│   ├── config.py                   # Configuration loader & CLI parser
│   ├── data_generators.py          # Main data generation engine
│   ├── schema_parser.py            # Schema parsing (CSV & JSON)
│   ├── util.py                     # Utility functions for data generation
│   ├── sample.csv                  # Example schema in CSV format
│   ├── sample.json                 # Example schema in JSON format
│   └── *.csv                       # Generated output files
├── tests/                          # Test suite
├── README.md                       # This file
├── requirements.txt                # Python dependencies
├── pyproject.toml                  # Black formatter & project config
└── .editorconfig                   # Cross-editor indentation standards
```

---

## Installation

### Prerequisites

- Python 3.9+
- pip or similar package manager

### Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Dependencies include:**
   - `pyjson5`: For JSON5 config file support
   - `faker`: For generating realistic random names and data
   - `black`: For code formatting (dev dependency)

3. **Format code (optional):**
   ```bash
   black .
   ```

---

## Usage

### Command Line

```bash
python3 schema_csv_gen/data_generators.py <schema_file> <output_file> [OPTIONS]
```

#### Required Arguments
- `schema_file`: Path to schema definition (.csv or .json)
- `output_file`: Path to output CSV file

#### Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--mode` | `-m` | str | Write mode: `overwrite` (o) or `append` (a). Default: `overwrite` |
| `--rows` | `-r` | int | Number of data rows to generate |
| `--null_percentage` | `-np` | int | Probability (0-100) that a nullable field will be null |
| `--seed` | `-s` | int | Random seed for reproducible results |
| `--integer_range` | `-ir` | int int | Lower and upper bounds for integer fields |
| `--float_range` | `-fr` | float float | Lower and upper bounds for float fields |
| `--date_range` | `-dr` | date date | Lower and upper bounds for date fields (YYYY-MM-DD) |
| `--timestamp_range` | `-tr` | datetime datetime | Lower and upper bounds for timestamp fields |
| `--config` | | str | Path to custom config file (JSON5 format) |

#### Examples

```bash
# Generate 50 rows, overwrite existing file
python3 schema_csv_gen/data_generators.py schema_csv_gen/sample.csv output.csv --rows 50 --mode o

# Generate with seed for reproducibility
python3 schema_csv_gen/data_generators.py schema_csv_gen/sample.csv output.csv --rows 100 --seed 42

# Generate with custom ranges
python3 schema_csv_gen/data_generators.py schema_csv_gen/sample.csv output.csv \
  --rows 20 \
  --integer_range 100 1000 \
  --float_range 50.0 500.0

# Append to existing file
python3 schema_csv_gen/data_generators.py schema_csv_gen/sample.csv output.csv \
  --rows 10 \
  --mode append
```

### As a Python Module

```python
from schema_csv_gen.data_generators import CreateData

# Generate data using default config
data = CreateData()
data.load()
```

---

## Configuration

### config.json

The tool automatically loads `config.json` from the current directory if available. Command-line arguments override config file values.

#### Example config.json

```json
{
  "default_rows": 20,
  "default_null_percentage": 80,
  "seed": null,
  "integer_range": [10, 1000],
  "float_range": [10.0, 1000.0],
  "date_range": ["2024-04-09", "2027-04-09"],
  "timestamp_range": ["2024-04-09T00:00:00", "2027-04-09T23:59:59"]
}
```

#### Configuration Fields

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `default_rows` | int | Number of rows to generate | 10 |
| `default_null_percentage` | int | Probability (0-100) that a nullable field will be null | 10 |
| `seed` | int | Random seed (null = random) | null |
| `integer_range` | [int, int] | Lower and upper bounds for integer fields | [10, 1000] |
| `float_range` | [float, float] | Lower and upper bounds for float fields | [10.0, 1000.0] |
| `date_range` | [str, str] | Lower and upper bounds for date fields | today ± 1 year |
| `timestamp_range` | [str, str] | Lower and upper bounds for timestamp fields | today ± 1 year |

---

## Schema Format

### CSV Schema

**File structure:** `sample.csv`

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| f_name | string | Yes | Field name (column name in output CSV) |
| f_type | string | Yes | Data type (see [Field Types](#field-types)) |
| f_nullable | boolean | Yes | Can this field be null? (`true` or `false`, case-insensitive) |
| f_start | int/string | No | Start value for auto-increment, or "na" for other types |
| f_length | int/string | No | Max length for string fields, or "na" for other types |
| f_values | string | No | Pipe-separated list of values for `valuetype` fields |

**Example:**
```csv
f_name,f_type,f_nullable,f_start,f_length,f_values
id,Autoincrementtype,false,97531,,
firstname,stringtype,false,1,50,
email,stringtype,true,1,80,
status,valuetype,false,na,na,"active|inactive|pending"
salary,floattype,false,,,
address,stringtype,true,1,200,
```

### JSON Schema

**File structure:** `sample.json`

```json
{
  "fields": [
    {
      "name": "id",
      "type": "Autoincrementtype",
      "nullable": false,
      "start": 97531,
      "length": 0,
      "values": ""
    },
    {
      "name": "firstname",
      "type": "stringtype",
      "nullable": false,
      "start": 1,
      "length": 50,
      "values": ""
    },
    {
      "name": "address",
      "type": "stringtype",
      "nullable": true,
      "start": 1,
      "length": 200,
      "values": ""
    }
  ]
}
```

---

## Field Types

All field types are **case-insensitive** in schema definitions.

### Basic Types

| Type | Description | Example Output |
|------|-------------|-----------------|
| `stringtype` | Random name from Faker library | "Michael Johnson" |
| `randomtexttype` | Random alphanumeric text | "aB3-cD9+eF=" |
| `integertype` | Random integer in configured range | 542 |
| `doubletype` | Random float (5 decimal places) | 234.56789 |
| `floattype` | Random float (5 decimal places) | 234.56789 |
| `booleantype` | Random boolean value | "True" or "False" |

### Date & Time Types

| Type | Description | Example Output |
|------|-------------|-----------------|
| `datetype` | Random date in configured range | "2025-06-15" |
| `timestamptype` | Random timestamp in configured range | "2025-06-15 14:32:45.123456" |

### Special Types

| Type | Description | Example Output |
|------|-------------|-----------------|
| `uuidtype` | Random UUID (version 1) | "e2f84d2a-a3bc-11ec-8456-001234567890" |
| `valuetype` | Random value from `f_values` list | "pending" (if f_values="active\|inactive\|pending") |
| `autoincrementtype` | Sequential integer starting from `f_start` | 97531, 97532, 97533, ... |

---

## Null Value Generation

### How Nulls Work

- **Only fields marked as nullable** (`f_nullable=true`) are eligible for null values.
- The `default_null_percentage` controls the probability that a nullable field will be set to null (empty string) **in each row**.
- Nulls are applied **per field, independently**. Each nullable field has its own random chance.
- **Auto-increment fields are never nullified**, regardless of `f_nullable` setting.

### Example Scenario

**Schema:**
```csv
f_name,f_type,f_nullable,f_start,f_length,f_values
id,Autoincrementtype,true,1,,
name,stringtype,false,1,50,
address,stringtype,true,1,100,
phone,stringtype,true,1,20,
email,stringtype,false,1,100,
```

**Configuration:**
- `default_null_percentage: 80`
- 5 fields total: 2 non-nullable, 3 nullable (plus auto-increment that ignores nulls)

**Result:**
- `id`: Never null (auto-increment)
- `name`: Always has value (not nullable)
- `address`: ~80% null, ~20% has value
- `phone`: ~80% null, ~20% has value
- `email`: Always has value (not nullable)

**Overall null rate:** ~32% of all cells are null (80% × 3 out of 5 fields)

### Key Points

- To increase overall nulls, mark more fields as nullable in your schema.
- Typos in `f_nullable` (e.g., `"fase"` instead of `"false"`) are treated as `true` (any non-"false"/"0"/None string is `true`).
- Use `--seed` to get reproducible null patterns.

---

## Code Modules

### config.py

Handles configuration loading from `config.json` and command-line argument parsing.

- **`load_config_file(file_path)`**: Loads JSON5 config, auto-detects `config.json`
- **`load_config()`**: Parses CLI arguments and merges with config file

### schema_parser.py

Parses schema definitions from CSV or JSON files.

- **`Parser.parse_schema(file_path)`**: Auto-detects format and parses
- **`Parser.parse_schema_csv(file_path)`**: CSV-specific parsing
- **`Parser.parse_schema_json(file_path)`**: JSON-specific parsing
- **`Parser.has_duplicate_names(records)`**: Validates unique field names

### data_generators.py

Main data generation engine.

- **`CreateData.__init__()`**: Initialize with config and auto-increment counter
- **`CreateData.create_file(schema)`**: Orchestrate file generation
- **`CreateData.create_item(schema)`**: Generate single row as dictionary
- **`handle_*type()` methods**: Field-specific generators (stringtype, integertype, floattype, etc.)

### util.py

Utility functions for data processing.

- **`Util.make_boolean(value)`**: Robust boolean conversion (handles typos)
- **`Util.get_random_date(start, end)`**: Generate random datetime in range
- **`Util.parse_date(date_str)`**: Parse flexible date strings

---

## Examples

### Example 1: Generate 20 Rows with 80% Nulls

```bash
python3 schema_csv_gen/data_generators.py schema_csv_gen/sample.csv output.csv \
  --rows 20 \
  --null_percentage 80
```

### Example 2: Reproducible Data with Seed

```bash
python3 schema_csv_gen/data_generators.py schema_csv_gen/sample.csv output1.csv --rows 10 --seed 12345
python3 schema_csv_gen/data_generators.py schema_csv_gen/sample.csv output2.csv --rows 10 --seed 12345
# output1.csv and output2.csv will be identical
```

### Example 3: Custom Integer and Float Ranges

```bash
python3 schema_csv_gen/data_generators.py schema_csv_gen/sample.csv output.csv \
  --rows 50 \
  --integer_range 1000 9999 \
  --float_range 100.0 1000.0
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| "No such file or directory: schema.csv" | Schema file path incorrect | Use absolute or relative path from execution directory |
| Output has fewer nulls than expected | Most fields not marked as nullable | Mark more fields with `f_nullable=true` in schema |
| TypeError: expected int or None | Config range values are strings | Use numeric values: `[10, 1000]` not `["10", "1000"]` |
| Duplicate field names | Schema has repeated field names | Ensure each field has unique `f_name` |
| Data varies each run | Seed not set | Use `--seed` to fix random generation |

---

## Code Quality

- **Formatter:** Black (line length: 120)
- **Linter:** Ruff (line length: 120)
- **Python:** 3.9+ type hints and modern syntax
- **Indentation:** 4 spaces (enforced via .editorconfig)

---

## License

View LICENSE file for details.

---

## Version History

- **v1.0** (April 2026): Initial release with CSV and JSON schema support, null value control, and 11+ field types
