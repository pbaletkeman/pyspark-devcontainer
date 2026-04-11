# PySpark Schema-to-CSV Generator: Work Plan

This plan breaks down the project into clear, actionable steps. Each part has a defined start and end, with explanations and input/output examples where needed.

---

## 1. Project Initialization

**Start:** Create the project structure and initialize version control.
**End:** All folders and placeholder files exist; `git` initialized.

**Steps:**
- Create the directory structure as outlined in the plan.
- Add `README.md`, `requirements.txt`, and `setup.py`.
- Initialize a Git repository.

**Input Example:**
No input required; this is setup.

**Output Example:**
```
pyspark-schema-csv-generator/
├── src/schema_csv_gen/
├── tests/
├── examples/
├── setup.py
├── requirements.txt
└── README.md
```

---

## 2. Schema Parsing Module

**Start:** Begin implementing `schema_parser.py` to read and parse schema files.
**End:** Can parse both JSON and text schema formats into a standard Python structure.

**Steps:**
- Implement functions to read and validate JSON schema files.
- Implement functions to parse the DSL-style text schema.
- Handle errors for malformed files and unsupported types.

**Input Example:**
JSON schema:
```json
{
  "fields": [
    {"name": "id", "type": "Autoincrementtype", "nullable": false, "start": 1}
  ]
}
```
Text schema:
```
id Autoincrementtype NOT NULL START 1
```

**Output Example:**
```python
[{"name": "id", "type": "Autoincrementtype", "nullable": False, "start": 1}]
```

---

## 3. Configuration Management

**Start:** Implement `config.py` to handle default settings and CLI overrides.
**End:** Can load defaults from `config.json` and override with CLI arguments.

**Steps:**
- Parse `config.json` for default settings.
- Merge CLI arguments, giving them precedence.
- Validate configuration values (e.g., null percentage 0-100).

**Input Example:**
`config.json`:
```json
{"default_rows": 100, "default_null_percentage": 10}
```
CLI: `--rows 200 --null-percentage 20`

**Output Example:**
Final config:
```python
{"rows": 200, "null_percentage": 20}
```

---

## 4. Data Generation Logic

**Start:** Implement `data_generators.py` for each supported type.
**End:** Can generate random data for all types, respecting nullability and config.

**Steps:**
- Use `faker` for strings, `random` for numbers/booleans, `uuid` for UUIDs.
- Implement date/timestamp range logic.
- Handle null value generation per field and global percentage.
- Support static/categorical values from config.

**Input Example:**
Field: `{ "name": "salary", "type": "FloatType", "nullable": True }`

**Output Example:**
Possible values: `1234.56`, `-999.99`, `None` (if null is chosen)

---

## 5. Core Generator

**Start:** Implement `generator.py` to combine schema, config, and data generators.
**End:** Can generate a list of rows (dicts) matching the schema.

**Steps:**
- For each row, generate values for all fields.
- Apply null logic and auto-increment where needed.
- Collect rows for CSV output.

**Input Example:**
Schema: `[{"name": "id", "type": "Autoincrementtype", "nullable": False, "start": 1}]`
Rows: `3`

**Output Example:**
```python
[{"id": 1}, {"id": 2}, {"id": 3}]
```

---

## 6. CSV Output

**Start:** Implement CSV writing logic in `generator.py` or a helper.
**End:** Can write generated rows to a CSV file with proper quoting/escaping.

**Steps:**
- Use Python’s `csv` module.
- Ensure correct handling of nulls, special characters, and quoting.

**Input Example:**
Rows: `[{"id": 1, "name": "Alice"}, {"id": 2, "name": None}]`

**Output Example:**
CSV file:
```
id,name
1,Alice
2,
```

---

## 7. CLI Interface

**Start:** Implement `cli.py` for argument parsing and entry point.
**End:** User can run the tool from the command line with all required options.

**Steps:**
- Use `argparse` to define all CLI arguments.
- Validate required arguments and show help.
- Connect CLI to generator and config modules.

**Input Example:**
Command:
```
python -m schema_csv_gen --schema schema.json --output data.csv --rows 10
```

**Output Example:**
A CSV file `data.csv` with 10 rows.

---

## 8. Logging and Error Handling

**Start:** Add logging and error handling throughout the codebase.
**End:** All errors are logged clearly; info/debug logs are available.

**Steps:**
- Use Python’s `logging` module.
- Log progress, errors, and debug info as specified.
- Ensure all user-facing errors are actionable.

**Input Example:**
Malformed schema file.

**Output Example:**
Log:
```
[2026-04-09 10:00:00] [ERROR] Invalid schema file: missing 'fields' key
```

---

## 9. Testing

**Start:** Write tests in the `tests/` directory for all modules and edge cases.
**End:** All core logic is covered by tests; edge cases are validated.

**Steps:**
- Test schema parsing, data generation, config merging, and CSV output.
- Test edge cases: all fields nullable, no fields nullable, large row counts, etc.

**Input Example:**
Test schema with all fields nullable.

**Output Example:**
Test passes if nulls are generated according to config.

---

## 10. Documentation

**Start:** Write a comprehensive `README.md` and example files.
**End:** Users can understand setup, usage, and configuration.

**Steps:**
- Document installation, CLI usage, config, and schema formats.
- Provide example schemas and configs in `examples/`.

**Input Example:**
User reads `README.md`.

**Output Example:**
User can run:
```
python -m schema_csv_gen --schema examples/schema_example.json --output out.csv
```

---

## 11. Packaging

**Start:** Finalize `setup.py` and `requirements.txt` for pip installation.
**End:** Project can be installed and run as a module.

**Steps:**
- Ensure all dependencies are listed.
- Test installation via `pip install .`

**Input Example:**
`pip install .`

**Output Example:**
Module is available as `schema_csv_gen`.

---

## 12. Final Review and Polish

**Start:** Review code, clean up, and ensure all requirements are met.
**End:** Project is ready for release or handoff.

**Steps:**
- Check for missing features or documentation.
- Run all tests and example commands.
- Polish code and comments.

---

**You can follow this plan step by step to build the tool efficiently.**
