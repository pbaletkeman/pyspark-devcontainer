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
    - [CSV Schema Format](#csv-schema-format)
      - [Required Columns (Must Always Be Present)](#required-columns-must-always-be-present)
      - [Optional Columns (Behavior Depends on Field Type)](#optional-columns-behavior-depends-on-field-type)
      - [CSV Schema Example with All Types](#csv-schema-example-with-all-types)
      - [CSV Special Cases and Common Errors](#csv-special-cases-and-common-errors)
    - [JSON Schema Format](#json-schema-format)
      - [Schema Structure](#schema-structure)
      - [Required Properties (Must Always Be Present)](#required-properties-must-always-be-present)
      - [Optional Properties](#optional-properties)
      - [JSON Schema Example with All Types](#json-schema-example-with-all-types)
      - [JSON Common Errors and Fixes](#json-common-errors-and-fixes)
    - [CSV vs JSON Comparison](#csv-vs-json-comparison)
    - [Schema Validation Rules](#schema-validation-rules)
  - [Field Types](#field-types)
    - [Basic Types](#basic-types)
      - [`stringtype`](#stringtype)
      - [`randomtexttype`](#randomtexttype)
      - [`integertype`](#integertype)
      - [`doubletype`](#doubletype)
      - [`floattype`](#floattype)
      - [`booleantype`](#booleantype)
    - [Date \& Time Types](#date--time-types)
      - [`datetype`](#datetype)
      - [`timestamptype`](#timestamptype)
    - [Special Types](#special-types)
      - [`uuidtype`](#uuidtype)
      - [`valuetype`](#valuetype)
      - [`autoincrementtype`](#autoincrementtype)
  - [Schema Column Requirements Summary](#schema-column-requirements-summary)
  - [Configuration Requirements](#configuration-requirements)
    - [config.json Field Validation](#configjson-field-validation)
    - [Valid config.json Example](#valid-configjson-example)
    - [Invalid Examples and Fixes](#invalid-examples-and-fixes)
  - [CLI Arguments Requirements](#cli-arguments-requirements)
    - [Type-Specific Validation](#type-specific-validation)
    - [CLI Examples with Validation](#cli-examples-with-validation)
  - [Null Value Generation](#null-value-generation)
    - [Configuration](#configuration-1)
    - [CLI Override](#cli-override)
    - [How It Works Internally](#how-it-works-internally)
    - [Critical Implementation Details](#critical-implementation-details)
    - [Important Rules](#important-rules)
    - [Default Behavior Notes](#default-behavior-notes)
    - [Examples](#examples-1)
    - [Troubleshooting Null Values](#troubleshooting-null-values)
  - [Code Modules](#code-modules)
    - [config.py](#configpy)
    - [schema\_parser.py](#schema_parserpy)
    - [data\_generators.py](#data_generatorspy)
    - [util.py](#utilpy)
  - [Examples](#examples-2)
    - [Example 1: Generate 20 Rows with 80% Nulls](#example-1-generate-20-rows-with-80-nulls)
    - [Example 2: Reproducible Data with Seed](#example-2-reproducible-data-with-seed)
    - [Example 3: Custom Integer and Float Ranges](#example-3-custom-integer-and-float-ranges)
  - [Troubleshooting](#troubleshooting)
  - [Code Quality](#code-quality)
  - [License](#license)
    - [Summary](#summary)
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

### CSV Schema Format

**File structure:** `sample.csv` - comma or tab-separated values

#### Required Columns (Must Always Be Present)

1. **f_name** (string)
   - Field name that appears as column header in output CSV
   - Must be unique across all fields in the schema
   - Any alphanumeric string, underscores allowed (e.g., "customer_id", "first_name", "brt_requested_amount")
   - Cannot be empty

2. **f_type** (string)
   - Data type for the field (see Field Types section)
   - Case-insensitive: "StringType", "stringtype", "STRINGTYPE" all work
   - Must be one of the 11 supported types
   - Cannot be empty

3. **f_nullable** (boolean)
   - Determines if field is eligible for null values
   - Valid values: `true`, `false`, `True`, `False`, `TRUE`, `FALSE` (case-insensitive)
   - Typos and other strings: Anything other than exactly "false" or "0" is treated as `true`
   - Examples:
     - `true` → Field can be null ✓
     - `false` → Field cannot be null ✓
     - `fase` → Treated as `true` (typo!) ⚠️
     - `False` → Treated as `true` (capital F!) ⚠️
     - Empty string → Treated as `true` ⚠️

#### Optional Columns (Behavior Depends on Field Type)

4. **f_start** (string or integer)
   - **For autoincrementtype:** First value in sequence (REQUIRED for autoincrementtype)
     - Example: `"97531"` → generates 97531, 97532, 97533...
   - **For other types:** Ignored (leave empty or use "na")
   - Can be any integer
   - If missing/empty: defaults to 0 for autoincrementtype (not recommended)

5. **f_length** (string or integer)
   - **For stringtype:** Maximum length to truncate generated name
     - Example: `50` → truncates to first 50 characters
     - Required for consistent output
   - **For randomtexttype:** Exact length of generated text
     - Example: `15` → always generates exactly 15 characters
     - Required for randomtexttype
   - **For other types:** Ignored (leave empty or use "na")
   - If missing/empty for stringtype: returns full name (variable length 10-30 chars)
   - If missing/empty for randomtexttype: defaults to 10 characters

6. **f_values** (string)
   - **For valuetype:** Pipe-separated list of possible values (REQUIRED for valuetype)
     - Example: `"active|inactive|pending"` → randomly selects one
     - Whitespace around pipes is trimmed: `" active | inactive "` → `"active"`, `"inactive"`
     - Can contain special characters, numbers, etc.
     - Example: `"CA000001|CA000002|CA000003"`
   - **For other types:** Ignored (leave empty)
   - If missing/empty for valuetype: returns empty string (not recommended)

#### CSV Schema Example with All Types

```csv
f_name,f_type,f_nullable,f_start,f_length,f_values
id,autoincrementtype,false,97531,,
firstname,stringtype,false,,50,
lastname,stringtype,false,,50,
description,randomtexttype,false,,100,
age,integertype,false,,,
salary,floattype,false,,,
is_active,booleantype,false,,,
birth_date,datetype,true,,,
created_at,timestamptype,false,,,
request_id,uuidtype,false,,,
country,valuetype,false,na,na,"US|CA|UK|AU"
```

#### CSV Special Cases and Common Errors

| Scenario | CSV Content | Result |
|----------|-------------|--------|
| Trailing spaces | `"true "` | Treated as `"true"` ✓ (auto-trimmed) |
| Wrong case for false | `"False"` | Treated as `true` ⚠️ (must be lowercase "false") |
| Empty f_nullable | `` | Treated as `true` ⚠️ (defaults to nullable) |
| valuetype with empty values | `""` | No values selected, always generates empty string ⚠️ |
| stringtype with empty length | `` | Returns full random name (10-30 chars) ⚠️ |
| randomtexttype with empty length | `` | Defaults to 10 characters ⚠️ |
| autoincrementtype with empty start | `` | Starts at 0 ⚠️ (not recommended) |
| Duplicate f_name | Multiple fields with same name | Error: "duplicate field in schema" ✗ |

---

### JSON Schema Format

**File structure:** `sample.json` - JSON5 format

#### Schema Structure

```json
{
  "fields": [
    {
      "name": "field_name",
      "type": "fieldtype",
      "nullable": boolean,
      "start": value,
      "length": value,
      "values": "string"
    },
    ...
  ]
}
```

#### Required Properties (Must Always Be Present)

1. **name** (string)
   - JSON equivalent of `f_name`
   - Must be unique
   - Example: `"customer_id"`, `"email_address"`

2. **type** (string)
   - JSON equivalent of `f_type`
   - Case-insensitive
   - Must be one of 11 supported types
   - Example: `"stringtype"`, `"IntegerType"`, `"FLOATTYPE"`

3. **nullable** (boolean)
   - JSON native boolean (not string)
   - Valid values: `true`, `false` (MUST use lowercase, no quotes)
   - INVALID: `"true"`, `"false"` (these are strings, not booleans!)
   - Example: `"nullable": true` ✓ vs `"nullable": "true"` ✗

#### Optional Properties

4. **start** (integer or string)
   - JSON equivalent of `f_start`
   - For autoincrementtype: first value in sequence (REQUIRED)
   - For other types: ignored
   - Can be integer or "na"
   - Example: `"start": 97531` or `"start": "na"`

5. **length** (integer or string)
   - JSON equivalent of `f_length`
   - For stringtype/randomtexttype: character length
   - For other types: ignored
   - Can be integer or "na"
   - Example: `"length": 50` or `"length": "na"`

6. **values** (string)
   - JSON equivalent of `f_values`
   - Pipe-separated list for valuetype
   - Empty string for other types
   - NOTE: Must be string, not array
   - Example: `"values": "active|inactive|pending"` ✓ vs `"values": ["active", "inactive"]` ✗

#### JSON Schema Example with All Types

```json
{
  "fields": [
    {
      "name": "id",
      "type": "autoincrementtype",
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
      "name": "lastname",
      "type": "stringtype",
      "nullable": false,
      "start": 1,
      "length": 50,
      "values": ""
    },
    {
      "name": "description",
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
      "name": "salary",
      "type": "floattype",
      "nullable": false,
      "start": 0,
      "length": 0,
      "values": ""
    },
    {
      "name": "is_active",
      "type": "booleantype",
      "nullable": false,
      "start": 0,
      "length": 0,
      "values": ""
    },
    {
      "name": "birth_date",
      "type": "datetype",
      "nullable": true,
      "start": 0,
      "length": 0,
      "values": ""
    },
    {
      "name": "created_at",
      "type": "timestamptype",
      "nullable": false,
      "start": 0,
      "length": 0,
      "values": ""
    },
    {
      "name": "request_id",
      "type": "uuidtype",
      "nullable": false,
      "start": 0,
      "length": 0,
      "values": ""
    },
    {
      "name": "country",
      "type": "valuetype",
      "nullable": false,
      "start": 0,
      "length": 0,
      "values": "US|CA|UK|AU"
    }
  ]
}
```

#### JSON Common Errors and Fixes

| Error | Invalid | Fix |
|-------|---------|-----|
| String boolean | `"nullable": "true"` | Use `"nullable": true` (no quotes) |
| Array for values | `"values": ["a", "b"]` | Use `"values": "a\|b"` (pipe-separated string) |
| Missing fields array | `{"fields": {...}}` | Use `{"fields": [...]}`  (array not object) |
| Quoted boolean | `"nullable": "false"` | Use `"nullable": false` (lowercase, no quotes) |
| String number for start | `"start": "123"` | Use `"start": 123` (integer, not string) |

---

### CSV vs JSON Comparison

| Aspect | CSV (sample.csv) | JSON (sample.json) |
|--------|------------------|-------------------|
| **Format Type** | Text-based, delimited | Structured, hierarchical |
| **Parsing Speed** | Faster | Slightly slower |
| **Type Validation** | All values are strings | Native types (bool, int, string) |
| **Boolean Values** | `true`/`false` (strings) | `true`/`false` (native booleans) |
| **Range Values** | Comma-separated or space-separated | JSON array or single values |
| **Comments** | Not supported | Supported in JSON5 |
| **Whitespace** | Trimmed automatically | Preserved (must trim manually) |
| **Default if Missing** | Empty string "" | Must specify all fields |
| **Learning Curve** | Easier for beginners | More explicit/strict |

---

### Schema Validation Rules

All schemas are validated when parsed:

1. **Duplicate field names:** Not allowed
   - Error: `"duplicate field in schema"`
   - Each field name must be unique across the entire schema

2. **Multiple auto-increment fields:** Not allowed
   - Error: `"duplicate field auto increment"`
   - Only one field can have type `autoincrementtype` per schema

3. **Field type case-insensitivity:** Case doesn't matter
   - `"stringtype"`, `"StringType"`, `"STRINGTYPE"` all work
   - Normalized internally to lowercase

4. **Required fields:** Must be present
   - `f_name`: REQUIRED
   - `f_type`: REQUIRED
   - `f_nullable`: REQUIRED
   - Other fields: OPTIONAL (leave empty if not needed)

---

---

## Field Types

All field types are **case-insensitive** in schema definitions. Each type has specific requirements for schema columns.

### Basic Types

#### `stringtype`
- **Description:** Generates random person names using the Faker library
- **Requirements:**
  - `f_values`: NOT USED (leave empty)
  - `f_length`: REQUIRED - Maximum length to truncate names. Recommended: 50-100
  - `f_start`: OPTIONAL - Ignored for this type
- **Example Schema:**
  ```csv
  f_name,f_type,f_nullable,f_start,f_length,f_values
  firstname,stringtype,false,,50,
  lastname,stringtype,false,,100,
  ```
- **Output Samples:** "Michael Johnson", "Sarah Williams", "James Brown"
- **Default Behavior:** If `f_length` is missing or empty, returns full name (typically 10-30 chars)

#### `randomtexttype`
- **Description:** Generates random alphanumeric text with special characters
- **Requirements:**
  - `f_values`: NOT USED (leave empty)
  - `f_length`: REQUIRED - Exact length of generated text (padding/truncation applied)
  - `f_start`: OPTIONAL - Ignored for this type
- **Character Set:** `a-z`, `0-9`, `-+*/=-|;:<>,.ABCDEFGHIJKLMNOPQRSTUVWXYZ`
- **Example Schema:**
  ```csv
  f_name,f_type,f_nullable,f_start,f_length,f_values
  reference_id,randomtexttype,false,,15,
  code,randomtexttype,false,,8,
  ```
- **Output Samples:** "aB3-cD9+eF=xYz", "K-L*M/N+O"
- **Default Behavior:** If `f_length` is 0 or missing, defaults to 10 characters

#### `integertype`
- **Description:** Generates random integers within configured range
- **Requirements:**
  - `f_values`: NOT USED (leave empty)
  - `f_length`: OPTIONAL - Not used for integer types
  - `f_start`: OPTIONAL - Not used for integer types
  - **Range Source:** Uses `integer_range` from config.json or `--integer_range` CLI arg
  - **Default Range:** [10, 1000] (if not specified in config)
- **Example Schema:**
  ```csv
  f_name,f_type,f_nullable,f_start,f_length,f_values
  employee_id,integertype,false,,,
  quantity,integertype,false,,,
  ```
- **Output Samples:** 542, 847, 123, 999
- **Config Override:** `python3 ... --integer_range 1 100` (generates 1-100)

#### `doubletype`
- **Description:** Generates random decimal numbers (floats) with 5 decimal places
- **Requirements:**
  - `f_values`: NOT USED (leave empty)
  - `f_length`: OPTIONAL - Not used
  - `f_start`: OPTIONAL - Not used
  - **Range Source:** Uses `float_range` from config.json or `--float_range` CLI arg
  - **Default Range:** [10.0, 1000.0] (if not specified in config)
  - **Precision:** Always 5 decimal places (e.g., 234.56789)
- **Example Schema:**
  ```csv
  f_name,f_type,f_nullable,f_start,f_length,f_values
  price,doubletype,false,,,
  balance,doubletype,false,,,
  ```
- **Output Samples:** 234.56789, 645.12345, 999.99999
- **Config Override:** `python3 ... --float_range 50.0 500.0` (generates 50.0-500.0)

#### `floattype`
- **Description:** Identical to `doubletype` - generates random decimal numbers with 5 decimal places
- **Requirements:** Same as `doubletype`
- **Example Schema:**
  ```csv
  f_name,f_type,f_nullable,f_start,f_length,f_values
  amount,floattype,false,,,
  rate,floattype,false,,,
  ```
- **Output Samples:** 456.78901, 123.45678, 789.01234
- **Note:** `doubletype` and `floattype` are functionally identical; use either based on your preference

#### `booleantype`
- **Description:** Generates random boolean values (true or false)
- **Requirements:**
  - `f_values`: NOT USED (leave empty)
  - `f_length`: OPTIONAL - Not used
  - `f_start`: OPTIONAL - Not used
- **Example Schema:**
  ```csv
  f_name,f_type,f_nullable,f_start,f_length,f_values
  is_active,booleantype,false,,,
  is_verified,booleantype,true,,,
  ```
- **Output Samples:** "True", "False"
- **Probability:** 50% true / 50% false (randomly distributed)

### Date & Time Types

#### `datetype`
- **Description:** Generates random dates within configured range, formatted as YYYY-MM-DD
- **Requirements:**
  - `f_values`: NOT USED (leave empty)
  - `f_length`: OPTIONAL - Not used
  - `f_start`: OPTIONAL - Not used
  - **Range Source:** Uses `date_range` from config.json or `--date_range` CLI arg
  - **Default Range:** Today ± 1 year (if not specified in config)
  - **Format Required:** "YYYY-MM-DD" in config and CLI args
- **Example Schema:**
  ```csv
  f_name,f_type,f_nullable,f_start,f_length,f_values
  birth_date,datetype,false,,,
  hire_date,datetype,false,,,
  ```
- **Config Example:**
  ```json
  "date_range": ["2020-01-01", "2025-12-31"]
  ```
- **Output Sample:** "2025-06-15", "2022-11-03", "2024-09-22"
- **CLI Override:** `python3 ... --date_range 2020-01-01 2025-12-31`

#### `timestamptype`
- **Description:** Generates random timestamps within configured range, formatted as ISO 8601 with microseconds
- **Requirements:**
  - `f_values`: NOT USED (leave empty)
  - `f_length`: OPTIONAL - Not used
  - `f_start`: OPTIONAL - Not used
  - **Range Source:** Uses `timestamp_range` from config.json or `--timestamp_range` CLI arg
  - **Default Range:** Today ± 1 year (if not specified in config)
  - **Format Required:** ISO 8601 format "YYYY-MM-DDTHH:MM:SS" in config
  - **Output Format:** "YYYY-MM-DD HH:MM:SS.ffffff" (includes microseconds)
- **Example Schema:**
  ```csv
  f_name,f_type,f_nullable,f_start,f_length,f_values
  created_at,timestamptype,false,,,
  updated_at,timestamptype,true,,,
  ```
- **Config Example:**
  ```json
  "timestamp_range": ["2024-01-01T00:00:00", "2026-12-31T23:59:59"]
  ```
- **Output Sample:** "2025-06-15 14:32:45.123456", "2024-11-03 08:15:22.654321"
- **CLI Override:** `python3 ... --timestamp_range 2024-01-01T00:00:00 2026-12-31T23:59:59`

### Special Types

#### `uuidtype`
- **Description:** Generates random UUID (Universally Unique Identifier) version 1
- **Requirements:**
  - `f_values`: NOT USED (leave empty)
  - `f_length`: OPTIONAL - Not used
  - `f_start`: OPTIONAL - Not used
- **Example Schema:**
  ```csv
  f_name,f_type,f_nullable,f_start,f_length,f_values
  request_id,uuidtype,false,,,
  transaction_id,uuidtype,false,,,
  ```
- **Output Sample:** "e2f84d2a-a3bc-11ec-8456-001234567890", "a1b2c3d4-e5f6-11ec-9e5d-002a3a4a0b0c"
- **Format:** Standard UUID v1 format (8-4-4-4-12 hex digits)

#### `valuetype`
- **Description:** Generates random values from a predefined list of options
- **Requirements:**
  - `f_values`: **REQUIRED** - Pipe-separated list of possible values
  - `f_length`: OPTIONAL - Used as metadata only, not for value generation
  - `f_start`: OPTIONAL - Used as metadata only, not for value generation
  - **Separator:** Use `|` (pipe character) to separate multiple values
  - **Whitespace:** Leading/trailing spaces are automatically stripped from each value
- **Example Schema:**
  ```csv
  f_name,f_type,f_nullable,f_start,f_length,f_values
  status,valuetype,false,,,active|inactive|pending
  country,valuetype,false,na,na,"US|CA|UK|AU|NZ"
  color,valuetype,true,,,red|blue|green|yellow|black|white
  ```
- **CSV vs JSON Handling:**
  - **CSV:** Values are stored as-is: `active|inactive|pending`
  - **JSON:** Use escaped pipe or native JSON string: `"active|inactive|pending"`
- **Output Sample:** "active", "pending", "inactive", "US", "CA", "red", "blue"
- **Probability:** Each value has equal probability of being selected

#### `autoincrementtype`
- **Description:** Generates sequential integers that increment by 1 for each row
- **Requirements:**
  - `f_values`: NOT USED (leave empty)
  - `f_length`: OPTIONAL - Usually 0, not used
  - `f_start`: **REQUIRED** - Starting integer value for first row
  - **Safety:** Auto-increment fields are **NEVER** set to null, even if `f_nullable=true` and `default_null_percentage=100`
- **Example Schema:**
  ```csv
  f_name,f_type,f_nullable,f_start,f_length,f_values
  id,autoincrementtype,false,1,,
  record_id,autoincrementtype,false,97531,,
  seq,autoincrementtype,true,10000,,
  ```
- **Behavior:**
  - Row 1: Uses `f_start` value (e.g., if `f_start=1`, outputs 1)
  - Row 2: `f_start + 1` (outputs 2)
  - Row 3: `f_start + 2` (outputs 3)
  - And so on...
- **Output Example (f_start=97531):** 97531, 97532, 97533, 97534, ...
- **Note:** Counter is per-field; different auto-increment fields maintain separate counters
- **Recommendation:** Set `f_nullable=false` for auto-increment fields (nulls are prevented anyway)

---

## Schema Column Requirements Summary

| Column | Required | Valid Values | Example | Notes |
|--------|----------|--------------|---------|-------|
| `f_name` | YES | Any string (unique) | "customer_id" | Must be unique across schema |
| `f_type` | YES | See Field Types above | "stringtype" | Case-insensitive |
| `f_nullable` | YES | true, false, "true", "false" (case-insensitive) | "true" | Typos like "fase" treated as true |
| `f_start` | NO | Integer or "na" | 1, 97531, "na" | Used by autoincrementtype, ignored by others |
| `f_length` | NO | Integer or "na" | 50, 100, "na" | Required for stringtype/randomtexttype, ignored by others |
| `f_values` | NO | Pipe-separated list or empty | "active\|inactive\|pending", "" | Required for valuetype, ignored by others |

---

## Configuration Requirements

### config.json Field Validation

| Field | Type | Valid Range | Required | Default | Notes |
|-------|------|-------------|----------|---------|-------|
| `default_rows` | int | > 0 | NO | 10 | Number of data rows to generate |
| `default_null_percentage` | int | 0-100 | NO | 10 | Percentage (as integer, 0-100, NOT 0.0-1.0) |
| `seed` | int or null | Any integer | NO | null | null = random generation each time |
| `integer_range` | [int, int] | Any integers | NO | [10, 1000] | [lower, upper] - both inclusive |
| `float_range` | [float, float] | Any floats | NO | [10.0, 1000.0] | [lower, upper] - both inclusive |
| `date_range` | [str, str] | YYYY-MM-DD format | NO | today ± 1 year | Must be valid dates in ISO format |
| `timestamp_range` | [str, str] | ISO 8601 format | NO | today ± 1 year | Format: "YYYY-MM-DDTHH:MM:SS" |

### Valid config.json Example

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

### Invalid Examples and Fixes

| Invalid | Problem | Fix |
|---------|---------|-----|
| `"default_null_percentage": 0.8` | Treated as integer 0 (wrong!) | Use `80` not `0.8` |
| `"date_range": ["04-09-2024", ...]` | Wrong date format | Use `"2024-04-09"` format |
| `"integer_range": ["10", "1000"]` | Strings instead of numbers | Use `[10, 1000]` without quotes |
| `"seed": "12345"` | String instead of int | Use `12345` without quotes |

---

## CLI Arguments Requirements

All CLI arguments override config.json values.

### Type-Specific Validation

| Argument | Type | Format | Example | Notes |
|----------|------|--------|---------|-------|
| `--rows` | int | Positive integer | `--rows 100` | Must be > 0 |
| `--null_percentage` | int | 0-100 | `--null_percentage 80` | Percentage, not decimal |
| `--seed` | int | Any integer | `--seed 42` | Space after `--seed` required |
| `--integer_range` | two ints | `<lower> <upper>` | `--integer_range 1 100` | Two space-separated integers |
| `--float_range` | two floats | `<lower> <upper>` | `--float_range 50.0 500.0` | Two space-separated floats |
| `--date_range` | two dates | `YYYY-MM-DD YYYY-MM-DD` | `--date_range 2024-01-01 2025-12-31` | Must be valid dates |
| `--timestamp_range` | two timestamps | ISO format | `--timestamp_range 2024-01-01T00:00:00 2025-12-31T23:59:59` | ISO 8601 required |

### CLI Examples with Validation

```bash
# VALID - All types correct
python3 schema_csv_gen/data_generators.py schema.csv out.csv \
  --rows 100 \
  --seed 42 \
  --null_percentage 80 \
  --integer_range 1 100 \
  --float_range 10.5 99.9

# INVALID - seed as string (will fail)
python3 schema_csv_gen/data_generators.py schema.csv out.csv --seed "12345"

# INVALID - null_percentage as decimal (treated as 0)
python3 schema_csv_gen/data_generators.py schema.csv out.csv --null_percentage 0.8

# VALID - date range with proper format
python3 schema_csv_gen/data_generators.py schema.csv out.csv \
  --date_range 2020-01-01 2025-12-31
```

---

## Null Value Generation

The system generates null values probabilistically for fields marked as `nullable: true`. Each field's null status is evaluated independently using a random threshold.

### Configuration

In `config.json`:
```json
{
  "default_null_percentage": 10.0
}
```

Valid range: 0.0 to 100.0
- **0.0%** = No nulls ever generated (even if field is nullable)
- **10.0%** = ~10% of nullable field instances will be null (DEFAULT)
- **50.0%** = ~50% of nullable field instances will be null
- **100.0%** = All nullable field instances will be null

### CLI Override

```bash
python main.py --rows 100 --schema sample.csv --null-threshold 20
```

Usage:
- Overrides the `default_null_percentage` from config.json
- Applies 20% null probability to all nullable fields
- Non-nullable fields are unaffected

### How It Works Internally

For each row generated, for each field:

1. Check if field has `f_nullable: true` (CSV) or `"nullable": true` (JSON)
2. If `false`: SKIP null check, always generate value
3. If `true`: Generate random decimal between 0.0 and 1.0
4. Compare: `random_value <= (null_percentage / 100.0)`
   - If TRUE: Set field to `null` (empty string in CSV)
   - If FALSE: Generate normal value
5. SPECIAL CASE: Even if field is nullable, if type is `autoincrementtype`, NEVER null

### Critical Implementation Details

**Per-Field Independence:**
- Each field gets its own random evaluation
- Row with 5 nullable fields: Each field independently evaluated
- Possible outcomes: 0 nulls, 1 null, 2 nulls, 3 nulls, 4 nulls, or 5 nulls per row

**Probability Calculation:**
- null_percentage from config: 10.0
- Convert to probability: 10.0 / 100.0 = 0.10
- Threshold comparison: `random.random() <= 0.10`
- Result: ~10% of evaluations return True

**AutoIncrement Safety:**
- Even if `autoincrementtype` field has `f_nullable: true`
- Null check explicitly skipped: `field_type != "autoincrementtype"`
- AutoIncrement counters ALWAYS increment, NEVER null

### Important Rules

1. **Non-nullable fields never null:** `f_nullable: false` → ALWAYS populated
2. **Per-field evaluation:** Each field independent (not row-level decision)
3. **AutoIncrement exception:** Never null, even if nullable=true
4. **CSV representation:** Null values appear as empty (no quotes, no "null" string)
5. **JSON representation:** Null values appear as empty strings or actual nulls in JSON
6. **Type-safe nulls:** Null fields preserve their type when regenerated

### Default Behavior Notes

**Before (Bug - Fixed):**
- Default was 0.0% → NO nulls generated despite nullable fields
- User expected 10% nulls but got 0%

**Current (Fixed):**
- Default is 10.0% → ~10% of nullable fields are null
- Matches user expectations

**Legacy Compatibility:**
- Old scripts with `--null-threshold 0` will still generate 0% nulls
- To disable nulls entirely: Use `--null-threshold 0`

### Examples

**Example 1: Climate Data with Weather Conditions**

Schema:
```csv
f_name,f_type,f_nullable,f_start,f_length,f_values
station_id,autoincrementtype,false,101,,
temperature,integertype,false,,,
humidity,integertype,true,,,
wind_speed,doubletype,true,,,
rainfall,doubletype,true,,,
```

Config with 30% null threshold:
```json
{"default_null_percentage": 30.0}
```

Sample output (10 rows) - each field evaluated independently:
```
station_id,temperature,humidity,wind_speed,rainfall
101,65,48,12.5,0.3
102,72,,15.2,0.5
103,58,62,,1.2
104,71,,,0.8
105,80,71,8.3,
106,69,,9.1,
107,75,55,,
108,61,68,11.4,0.2
109,82,,,
110,70,,,0.9
```

Explanation:
- **station_id:** NEVER null (autoincrementtype) - always 101, 102, 103...
- **temperature:** NEVER null (f_nullable=false) - always populated
- **humidity:** ~30% null, ~70% populated
- **wind_speed:** ~30% null, ~70% populated
- **rainfall:** ~30% null, ~70% populated

Per-row breakdown:
- Row 1: All nullable fields populated (70% chance each occurred)
- Row 2: humidity=null, others populated
- Row 3: wind_speed=null, others populated
- Row 4: humidity and wind_speed null, rainfall populated
- Row 5: All populated
- Row 6: humidity and rainfall null, wind_speed populated

**Example 2: Null Threshold Impact on Data Density**

Same schema, different thresholds:

Threshold 0% (No Nulls):
```
101,65,48,12.5,0.3
102,72,51,15.2,0.5
103,58,62,9.8,1.2
```
All fields always populated. Use for: Testing null-free scenarios, baseline data.

Threshold 10% (Default):
```
101,65,48,,0.3
102,72,,15.2,0.5
103,58,62,9.8,
```
Few nulls, realistic data. Use for: Normal data generation with occasional missing values.

Threshold 50% (Moderate):
```
101,65,,12.5,
102,72,,,0.5
103,,62,,1.2
```
Many nulls throughout. Use for: Testing null handling, data quality checks.

Threshold 100% (All Nulls):
```
101,65,,,,
102,72,,,,
103,,,,
```
All nullable always null. Use for: Edge case testing, error handling validation.

**Example 3: Field Type Null Behavior**

When null value generated for a field, representation depends on type and format:

CSV Output:
```
stringtype_field,integertype_field,datetype_field,valuetype_field
"Alice",42,2023-01-15,"active"
"Bob",,2023-01-16,
"Charlie",88,,
,99,2023-01-18,"pending"
```

JSON Output:
```json
[
  {"stringtype_field": "Alice", "integertype_field": 42, "datetype_field": "2023-01-15", "valuetype_field": "active"},
  {"stringtype_field": "Bob", "integertype_field": null, "datetype_field": "2023-01-16", "valuetype_field": null},
  {"stringtype_field": "Charlie", "integertype_field": 88, "datetype_field": null, "valuetype_field": null},
  {"stringtype_field": null, "integertype_field": 99, "datetype_field": "2023-01-18", "valuetype_field": "pending"}
]
```

Null behavior per type:
- **stringtype:** Null = empty field in CSV, null in JSON
- **integertype:** Null = empty field in CSV, null in JSON
- **datetype:** Null = empty field in CSV, null in JSON
- **valuetype:** Null = empty field in CSV, null in JSON
- **NEVER null:** autoincrementtype (counter continues)

**Example 4: Configuration Priority (Precedence Order)**

From highest to lowest priority:

1. **CLI argument `--null-threshold XX` (Highest Priority)**
   ```bash
   python main.py --null-threshold 25  # Uses 25%, ignores config.json
   ```

2. **config.json value `default_null_percentage`**
   ```json
   {"default_null_percentage": 30.0}
   ```

3. **Hardcoded default (Lowest Priority)**
   - 10.0% if nothing specified

Example execution flow:
```bash
# Uses config.json value (30%)
python main.py --rows 100 --schema sample.csv

# Overrides config.json with CLI value (50%)
python main.py --rows 100 --schema sample.csv --null-threshold 50

# Uses hardcoded default (10%) if config.json not found
python main.py --rows 100 --schema sample.csv  # (if no config.json in cwd)
```

### Troubleshooting Null Values

| Issue | Cause | Solution |
|-------|-------|----------|
| No nulls in output | `default_null_percentage: 0.0` in config or `--null-threshold 0` | Change to 10.0+, use `--null-threshold 10` |
| Too many nulls | `default_null_percentage` too high (e.g., 100) | Reduce to 10-30% for realistic data, use `--null-threshold 25` |
| AutoIncrement has nulls | Shouldn't happen (field type check prevents it) | Verify using latest code version |
| All rows have all nulls | `--null-threshold 100` accidentally applied | Verify CLI args, reduce threshold, use `--null-threshold 10` |
| Some nullable fields never null | Random chance (~10% default) | Increase threshold to 50%+ to see more nulls consistently |
| Config.json ignored | File not detected or not in correct working directory | Use `--config ./config.json` or ensure file in working directory |
| Nulls inconsistent between runs | No seed specified (random each time) | Use `--seed 12345` for reproducible results |

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

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for complete details.

### Summary

- **License Type:** MIT
- **Copyright:** Copyright (c) 2026 pbaletkeman
- **Permissions:** Commercial use, modification, distribution, private use
- **Conditions:** License and copyright notice must be included
- **Limitations:** No liability or warranty

For full license text, refer to the LICENSE file in the repository root.

---

## Version History

- **v1.0** (April 2026): Initial release with CSV and JSON schema support, null value control, and 11+ field types
