#!/usr/bin/env python3
import json
import sys
from jsonschema import validate, ValidationError


def main(schema_path: str, data_path: str) -> None:
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError as e:
        print(f"[validate] Missing file: {e.filename}")
        sys.exit(1)

    try:
        validate(instance=data, schema=schema)
        print("[validate] JSON OK ✔")
    except ValidationError as e:
        print("[validate] JSON schema validation failed ❌")
        print("Path :", list(e.path))
        print("Error:", e.message)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: tools/validate_infographic.py <schema.json> <data.json>")
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
