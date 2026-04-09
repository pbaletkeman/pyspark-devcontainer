## Plan: Generate Sample CSV from PySpark Schema

You want a tool/script that:
- Reads a PySpark schema file (JSON or text format with field definitions)
- Generates a CSV file with random sample data matching the schema (correct types, plausible values)
- Supports customizable data generation with null values, static categories, and flexible configuration

---

## Implementation Requirements

### Core Functionality
1. Parse schema files (JSON or text format) to extract field names, types, and nullability
2. Generate random data matching each field's type using appropriate libraries
3. Support null values with user-configurable percentage (0-100%)
4. Allow static/categorical values for specific fields
5. Write output as CSV with proper escaping and quoting
6. No support for nested structures (flat schemas only)

### Supported Data Types
- **StringType**: Realistic data via Faker library (names, addresses, text)
- **IntegerType**: Random integers between -1000 and 1000 (configurable range via CLI or config file)
- **FloatType/DoubleType**: Random floats between -1000.00 and 1000.00 with 2 decimal places (configurable range via CLI or config file)
- **BooleanType**: Random true/false values
- **DateType**: Random dates between 2 years ago and 1 year from now (format: YYYY-MM-DD) (configurable range via CLI or config file)
- **TimestampType**: Random timestamps in same range (format: ISO 8601) (configurable range via CLI or config file)

### Schema File Formats

**JSON Format (Recommended)**
```json
{
  "fields": [
    {"name": "id", "type": "IntegerType", "nullable": false},
    {"name": "name", "type": "StringType", "nullable": false},
    {"name": "email", "type": "StringType", "nullable": true},
    {"name": "salary", "type": "FloatType", "nullable": true},
    {"name": "hire_date", "type": "DateType", "nullable": false},
    {"name": "is_active", "type": "BooleanType", "nullable": false}
  ]
}
```

**Text Format (DSL-style)**
```
id IntegerType NOT NULL
name StringType NOT NULL
email StringType NULLABLE
salary FloatType NULLABLE
hire_date DateType NOT NULL
is_active BooleanType NOT NULL
```

### Configuration File (Default Settings)
`config.json` - Override with CLI arguments
```json
{
  "default_rows": 100,
  "default_null_percentage": 10,
  "nullable_field_overrides": [],
  "seed": null,
  "categories": {
    "department": ["HR", "IT", "Finance", "Sales"],
    "status": ["Active", "Inactive"]
  },
  "integer_range": [-1000, 1000],
  "float_range": [-1000.0, 1000.0],
  "date_range": ["2024-04-09", "2027-04-09"],
  "timestamp_range": ["2024-04-09T00:00:00", "2027-04-09T23:59:59"]
}
```

### CLI Arguments
```
--schema FILE          (required) Path to schema file (JSON or text)
--output FILE          (required) Output CSV file path
--integer-range MIN,MAX        (optional) Integer range, e.g. --integer-range -1000,1000 (default: -1000,1000)
--float-range MIN,MAX          (optional) Float range, e.g. --float-range -1000.0,1000.0 (default: -1000.0,1000.0)
--date-range START,END         (optional) Date range, e.g. --date-range 2024-04-09,2027-04-09 (default: 2 years ago to 1 year from now)
--timestamp-range START,END    (optional) Timestamp range, e.g. --timestamp-range 2024-04-09T00:00:00,2027-04-09T23:59:59 (default: 2 years ago to 1 year from now)
--rows N               (optional) Number of rows to generate (default: 100)
--null-percentage N    (optional) Percentage of null values (0-100, default: 10)
--config FILE          (optional) Path to config file for defaults
--non-nullable-fields F1,F2,F3  (optional) Force fields to never be null
--seed N               (optional) Random seed for reproducible output
--help                 (optional) Display usage instructions
```

### Project Structure
```
pyspark-schema-csv-generator/
├── src/
│   └── schema_csv_gen/
│       ├── __init__.py
│       ├── cli.py              # CLI entry point & argument parsing
│       ├── generator.py        # Core data generation logic
│       ├── schema_parser.py    # Parse JSON/text schema files
│       ├── config.py           # Config file management
│       └── data_generators.py  # Type-specific data generation
├── tests/
│   ├── test_schema_parser.py
│   ├── test_generator.py
│   ├── test_config.py
│   └── test_edge_cases.py
├── examples/
│   ├── schema_example.json
│   ├── config_example.json
│   └── schema_example.txt
├── setup.py                    # Package setup for pip
├── requirements.txt
└── README.md
```

### Dependencies
```
pyspark >= 3.0.0
faker >= 40.13.0
python >= 3.8
```

### Null Value Handling
- Global null percentage applies uniformly to all nullable fields
- Fields marked as `nullable: false` in schema are never null
- `--non-nullable-fields` overrides schema definition for specific fields
- Null percentage is respected after respecting nullability constraints

### Error Handling
- **Invalid schema file**: Malformed JSON or unsupported DSL syntax
- **Unsupported types**: Display list of supported types
- **Missing required arguments**: Show usage with --help
- **Invalid null percentage**: Must be 0-100
- **Non-existent schema file**: Clear file not found error
- **Output path not writable**: Permission denied error
- All errors logged with clear, actionable messages

### Logging Strategy
- **Levels**: INFO (progress), DEBUG (details), ERROR (failures)
- **Output**: stdout + optional log file
- **Format**: `[TIMESTAMP] [LEVEL] message`
- **Info messages**: Starting generation, rows generated, completion time
- **Error messages**: Invalid schema, type mismatches, I/O issues

### Testing Edge Cases
- All fields nullable
- No fields nullable
- Mix of nullable/non-nullable
- Empty schema
- Unsupported data types
- Large row count (1M+) performance
- Unicode and special characters in string generation
- Boundary values for numeric types

### Example Usage
```bash
# Basic usage with defaults (100 rows, 10% nulls)
python -m schema_csv_gen --schema schema.json --output data.csv

# Custom rows and null percentage
python -m schema_csv_gen --schema schema.json --output data.csv --rows 1000 --null-percentage 25

# With config file for defaults
python -m schema_csv_gen --schema schema.json --output data.csv --config config.json

# Force specific fields to never be null
python -m schema_csv_gen --schema schema.json --output data.csv --non-nullable-fields "id,name,email"

# Reproducible output with seed
python -m schema_csv_gen --schema schema.json --output data.csv --seed 42

# Display help
python -m schema_csv_gen --help
```

### Implementation Notes
- Use Python's `csv` module for proper delimiter and quoting handling
- Use `faker` library for realistic string data generation
- Use `random` module for numeric/boolean generation
- Respect schema nullability by default; allow CLI overrides
- Package as pip-installable module for distribution
- Focus on core flat-schema functionality; design for future extensibility
- Provide comprehensive README with setup and usage examples
