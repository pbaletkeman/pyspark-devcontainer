# pyspark-schema-csv-generator

This project generates CSV files with random or schema-driven data for testing and development, using a configurable schema and options.

- [pyspark-schema-csv-generator](#pyspark-schema-csv-generator)
	- [Configuration Options](#configuration-options)
	- [Schema CSV Rows](#schema-csv-rows)
		- [Supported Data Types (f\_type)](#supported-data-types-f_type)
	- [Example Usage](#example-usage)
	- [Example Schema CSV](#example-schema-csv)
	- [Configuration File (config.json)](#configuration-file-configjson)
		- [Example config.json](#example-configjson)
		- [config.json Fields](#configjson-fields)
	- [Usage with Config File](#usage-with-config-file)
	- [Setup Instructions](#setup-instructions)
		- [Prerequisites](#prerequisites)
		- [Python Virtual Environment Setup](#python-virtual-environment-setup)
			- [Create a Virtual Environment](#create-a-virtual-environment)
			- [Install Dependencies](#install-dependencies)
			- [Deactivate Virtual Environment](#deactivate-virtual-environment)
		- [Dependencies](#dependencies)
			- [requirements.txt](#requirementstxt)
		- [Running the Generator](#running-the-generator)
	- [Sample Schema Files](#sample-schema-files)
		- [sample.csv - CSV Format Schema Definition](#samplecsv---csv-format-schema-definition)
		- [sample.json - JSON5 Format Schema Definition](#samplejson---json5-format-schema-definition)
		- [Comparing CSV vs JSON Schema Formats](#comparing-csv-vs-json-schema-formats)
		- [Creating Custom Schemas](#creating-custom-schemas)

## Configuration Options

Configuration can be provided via command-line arguments and/or a JSON5 config file. The main options are:

| Option                      | CLI Argument / Config Key         | Type      | Description                                                                                 |
|-----------------------------|-----------------------------------|-----------|---------------------------------------------------------------------------------------------|
| schema                      | positional (required)             | str       | Path to schema definition file (.json or .csv)                                              |
| output                      | positional (required)             | str       | Output CSV file path                                                                        |
| mode                        | --mode / mode                     | str       | Write mode: 'append', 'a', 'overwrite', 'o' (default: 'overwrite')                          |
| rows                        | --rows / default_rows             | int       | Number of data rows to generate                                                             |
| null_percentage             | --null_percentage / default_null_percentage | int | Percentage of null values in generated data (default: 5)                                    |
| nullable_field_overrides    | --nullable_field_overrides / nullable_field_overrides | list | Fields that cannot be null (comma-separated or list)                                        |
| seed                        | --seed / seed                     | int       | Random seed for reproducible results                                                        |
| integer_range               | --integer_range / integer_range   | list[int] | Lower and upper bounds for integer fields (default: [0, 10])                                |
| float_range                 | --float_range / float_range       | list[float]| Lower and upper bounds for float fields (default: [-10, 10])                                |
| date_range                  | --date_range / date_range         | list[str] | Lower and upper bounds for date fields (YYYY-MM-DD)                                         |
| timestamp_range             | --timestamp_range / timestamp_range | list[str] | Lower and upper bounds for timestamp fields (YYYY-MM-DDTHH:MM:SS)                           |
| config                      | --config                          | str       | Path to additional config file (JSON5)                                                      |

## Schema CSV Rows

A schema CSV file defines the structure of the generated data. Each row describes a field:

| Column      | Description                                                                 |
|-------------|-----------------------------------------------------------------------------|
| f_name      | Field name (column name in output CSV)                                      |
| f_type      | Data type (see below)                                                       |
| f_nullable  | Whether the field can be null (true/false)                                  |
| f_start     | (Optional) Start value for auto-increment fields                            |
| f_length    | (Optional) Max length for string or text fields                             |
| f_values    | (Optional) Pipe-separated list of possible values for 'valuetype' fields    |

### Supported Data Types (f_type)

- `AutoincrementtType`: Sequential integer, auto-incremented per row
- `StringType`: Random name (Faker)
- `RandomTextType`: Random text (Faker)
- `IntegerType`: Random integer in range
- `DoubleType`: Random float in range
- `FloatType`: Random float in range
- `BooleanType`: Random boolean (true/false)
- `DateType`: Random date in range
- `TimestampType`: Random timestamp in range
- `UUIDType`: Random UUID
- `ValueType`: Random value from provided list (see f_values)

## Example Usage

```sh
python data_generators.py sample.csv output.csv --rows 10000 --mode o
```

## Example Schema CSV

| f_name     | f_type           | f_nullable | f_start | f_length | f_values                                 |
|------------|------------------|------------|---------|----------|------------------------------------------|
| id         | AutoIncrementType| false      | 1       |          |                                          |
| firstname  | StringType       | false      |         | 50       |                                          |
| lastname   | RandomTextType   | false      |         | 100      |                                          |
| age        | IntegerType      | false      |         |          |                                          |
| color      | ValueType        | false      |         |          | green \| blue \| yellow \| black \| red \|

## Configuration File (config.json)

A JSON5 configuration file can be used to provide default values for data generation. Command-line arguments override config file values.

### Example config.json

```json
{
  "default_rows": 1000,
  "default_null_percentage": 5,
  "nullable_field_overrides": [],
  "seed": 12345,
  "integer_range": [-1000, 1000],
  "float_range": [-1000.0, 1000.0],
  "date_range": ["2024-01-01", "2026-12-31"],
  "timestamp_range": ["2024-01-01T00:00:00", "2026-12-31T23:59:59"]
}
```

### config.json Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| default_rows | int | Default number of rows to generate | 1000 |
| default_null_percentage | int | Percentage of null values in optional fields | 5 |
| nullable_field_overrides | list | Field names that should never be null | `["id", "firstname"]` |
| seed | int or null | Random seed for reproducible results (null = random) | 12345 |
| integer_range | [min, max] | Default range for integer fields | `[-1000, 1000]` |
| float_range | [min, max] | Default range for float fields | `[-1000.0, 1000.0]` |
| date_range | ["start", "end"] | Default date range (YYYY-MM-DD) | `["2024-01-01", "2026-12-31"]` |
| timestamp_range | ["start", "end"] | Default timestamp range (ISO format) | `["2024-01-01T00:00:00", "2026-12-31T23:59:59"]` |

## Usage with Config File

```sh
# Use config file with default values
python data_generators.py sample.csv output.csv --config config.json

# Override config file values with CLI arguments
python data_generators.py sample.csv output.csv --config config.json --rows 5000 --seed 999
```

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

### Python Virtual Environment Setup

It is recommended to use a Python virtual environment to isolate project dependencies. This prevents conflicts with system-wide Python packages.

#### Create a Virtual Environment

```sh
# Navigate to the project directory
cd pyspark-schema-csv-generator

# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

#### Install Dependencies

Once the virtual environment is activated, install the project dependencies:

```sh
# Install from requirements.txt
pip install -r requirements.txt

# Or install dependencies individually
pip install faker pyjson5
```

#### Deactivate Virtual Environment

When finished working on the project, deactivate the virtual environment:

```sh
deactivate
```

### Dependencies

The project requires the following Python packages:

| Package | Version | Purpose |
|---------|---------|---------|
| faker | Latest | Generates realistic random data (names, text, dates, etc.) |
| pyjson5 | Latest | Parses JSON5 configuration files with flexible syntax |

#### requirements.txt

```
faker
pyjson5
```

Create this file in the project root if it doesn't exist, then run `pip install -r requirements.txt`.

### Running the Generator

After setup, you can generate data using:

```sh
# Generate 10,000 rows using the sample schema
python src/schema_csv_gen/data_generators.py src/schema_csv_gen/sample.csv output.csv --rows 10000

# Generate with seed for reproducible results
python src/schema_csv_gen/data_generators.py src/schema_csv_gen/sample.csv output.csv --rows 10000 --seed 12345

# Generate with custom configuration
python src/schema_csv_gen/data_generators.py src/schema_csv_gen/sample.csv output.csv --config src/schema_csv_gen/config.json --rows 5000
```

## Sample Schema Files

### sample.csv - CSV Format Schema Definition

The `sample.csv` file is a tab-delimited CSV file that defines the schema for data generation. It demonstrates all 11 supported data types.

**File Location**: `src/schema_csv_gen/sample.csv`

**Structure**: Tab-separated values with headers: `f_name`, `f_type`, `f_nullable`, `f_start`, `f_length`, `f_values`

**Contents**:

| f_name | f_type | f_nullable | f_start | f_length | f_values |
|--------|--------|------------|---------|----------|----------|
| id | AutoincrementType | false | 541 | | (auto-incremented starting at 541) |
| firstname | StringType | false | 1 | 50 | (random names using Faker) |
| lastname | RandomTextType | false | 1 | 100 | (random text using Faker) |
| age | IntegerType | false | | | (random integers in default range: 0-10 or config range) |
| owning | DoubleType | false | | | (random double/float values) |
| winning | FloatType | false | | | (random float values) |
| single | BooleanType | false | | | (random true/false) |
| startDate | DateType | false | | | (random dates in default range: 2024-01-01 to 2026-12-31) |
| lunchTime | TimestampType | false | | | (random timestamps in default range) |
| color | ValueType | false | 1 | 100 | green \| blue \| yellow \| black \| cyan \| pink \| white \| red |

**Use Cases**:
- Simple text-based schema definition
- Easy to version control (plain text format)
- Human-readable and editable in any text editor
- Can be used directly with the data generator as a positional argument

**Example Command**:
```sh
python data_generators.py sample.csv output.csv --rows 10000
```

### sample.json - JSON5 Format Schema Definition

The `sample.json` file defines the same schema as `sample.csv` but in JSON5 format. This provides a more structured, programmatic approach to schema definition.

**File Location**: `src/schema_csv_gen/sample.json`

**Structure**: JSON5 object with "fields" array containing field definition objects

**Schema Object Structure**:

```json
{
  "fields": [
    {
      "name": "field_name",
      "type": "DataType",
      "nullable": false,
      "start": 0,
      "length": 50,
      "values": ""
    }
  ]
}
```

**Field Properties**:

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| name | string | The field name (column name in output CSV) | "firstname" |
| type | string | The data type for the field | "stringtype", "integertype", "datetype" |
| nullable | boolean | Whether the field can contain null values | false |
| start | integer | Start value for auto-increment or range-based types | 541 (for auto-increment), 1 (for ranges) |
| length | integer | Maximum length for string/text fields, or field width | 50 (string max length), 100 (value list max length) |
| values | string | Pipe-separated list of possible values for "valuetype" | "red \| blue \| green" |

**Complete sample.json Contents**:

```json
{
  "fields": [
    {
      "name": "id",
      "type": "Autoincrementtype",
      "nullable": false,
      "start": 541,
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
      "name": "lastname",
      "type": "randomtexttype",
      "nullable": false,
      "start": 1,
      "length": 100,
      "values": ""
    },
    {
      "name": "age",
      "type": "integertype",
      "nullable": false,
      "start": 0,
      "length": 0,
      "values": ""
    },
    {
      "name": "owning",
      "type": "doubletype",
      "nullable": false,
      "start": 0,
      "length": 0,
      "values": ""
    },
    {
      "name": "winning",
      "type": "floattype",
      "nullable": false,
      "start": 0,
      "length": 0,
      "values": ""
    },
    {
      "name": "single",
      "type": "booleantype",
      "nullable": false,
      "start": 0,
      "length": 0,
      "values": ""
    },
    {
      "name": "startDate",
      "type": "datetype",
      "nullable": false,
      "start": 0,
      "length": 0,
      "values": ""
    },
    {
      "name": "lunchTime",
      "type": "timestamptype",
      "nullable": false,
      "start": 0,
      "length": 0,
      "values": ""
    },
    {
      "name": "color",
      "type": "valuetype",
      "nullable": false,
      "start": 1,
      "length": 100,
      "values": "green | blue | yellow | black | cyan | pink | white | red"
    }
  ]
}
```

**Field Descriptions**:

1. **id** - Auto-incremented integer starting at 541. One row = +1.
2. **firstname** - Random person's first name (Faker library). Max 50 characters.
3. **lastname** - Random text (simulating last name). Max 100 characters.
4. **age** - Random integer in range. Uses config `integer_range` (default: 0-10).
5. **owning** - Random double (decimal number). Uses config `float_range` (default: -10.0 to 10.0).
6. **winning** - Random float (decimal number). Uses config `float_range` (default: -10.0 to 10.0).
7. **single** - Random boolean (true/false). 50% chance each value.
8. **startDate** - Random date in range. Uses config `date_range` (default: 2024-01-01 to 2026-12-31). Format: YYYY-MM-DD.
9. **lunchTime** - Random timestamp in range. Uses config `timestamp_range` (default: 2024-01-01T00:00:00 to 2026-12-31T23:59:59). Format: ISO 8601.
10. **color** - Random value from predefined list. Options: green, blue, yellow, black, cyan, pink, white, red.

**Use Cases**:
- Programmatic schema definition (can be generated dynamically)
- More control over field properties
- Supports comments and flexible JSON5 syntax
- Easier integration with configuration management systems
- Better for complex schema definitions

**Example Command**:
```sh
python data_generators.py sample.json output.csv --rows 10000 --seed 12345
```

### Comparing CSV vs JSON Schema Formats

| Aspect | CSV (sample.csv) | JSON (sample.json) |
|--------|------------------|-------------------|
| **Format** | Tab-separated values | JSON5 objects |
| **Readability** | Compact, simple | Verbose but structured |
| **Parsing Speed** | Fast | Slightly slower |
| **Data Types** | All values are strings | Native JSON types |
| **Comments** | Not supported | Supported (JSON5) |
| **Complexity** | Limited functionality | Full property control |
| **Use Case** | Quick/simple schemas | Production/complex schemas |

Both formats parse identically by the data generator. Use whichever format fits your workflow.

### Creating Custom Schemas

You can create your own schema files using either format:

**CSV Format**:
```
f_name	f_type	f_nullable	f_start	f_length	f_values
user_id	Autoincrementtype	false	1000
email	stringtype	false	1	100
status	valuetype	false	1	20	active | inactive | pending
```

**JSON Format**:
```json
{
  "fields": [
    {"name": "user_id", "type": "Autoincrementtype", "nullable": false, "start": 1000, "length": 0, "values": ""},
    {"name": "email", "type": "stringtype", "nullable": false, "start": 1, "length": 100, "values": ""},
    {"name": "status", "type": "valuetype", "nullable": false, "start": 1, "length": 20, "values": "active | inactive | pending"}
  ]
}
```
