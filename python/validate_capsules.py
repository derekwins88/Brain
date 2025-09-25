#!/usr/bin/env python3
"""
Validate Brain capsules against JSON Schema with friendly output and
GitHub Actions annotations.

Ignored by design:
  - Any file starting with an underscore:   capsules/_*.json (templates, scratch)
  - Any file with JSONC extension:          capsules/*.jsonc (contains comments)
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from typing import List, Tuple

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "capsule.schema.json"
CAPSULE_DIR = ROOT / "capsules"


def load_schema() -> dict:
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def discover_files() -> Tuple[List[Path], List[Path]]:
    """
    Returns (to_validate, ignored)
      - to_validate: *.json that do NOT start with '_' (e.g., brain-*.json)
      - ignored: _*.json and all *.jsonc
    """
    if not CAPSULE_DIR.exists():
        return [], []
    json_files = sorted(p for p in CAPSULE_DIR.glob("*.json") if p.is_file())
    jsonc_files = sorted(p for p in CAPSULE_DIR.glob("*.jsonc") if p.is_file())

    ignored = [p for p in json_files if p.name.startswith("_")]
    to_validate = [p for p in json_files if not p.name.startswith("_")]
    ignored.extend(jsonc_files)
    return to_validate, sorted(ignored)


def validate_file(validator: Draft202012Validator, path: Path) -> Tuple[bool, List[str]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:  # pragma: no cover - user feedback path
        return False, [f"JSON parse error: {e}"]

    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    if not errors:
        return True, []
    msgs = []
    for err in errors:
        path_elems = []
        for x in err.path:
            if isinstance(x, int):
                path_elems.append(f"[{x}]")
            else:
                path_elems.append(f".{x}")
        loc = "$" + "".join(path_elems)
        msgs.append(f"{loc}: {err.message}")
    return False, msgs


def annotate_github(path: Path, messages: List[str]) -> None:
    for msg in messages:
        print(f"::error file={path}::{msg}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Brain capsules against JSON Schema."
    )
    parser.add_argument(
        "--json",
        dest="json_out",
        type=Path,
        help="Write machine-readable summary JSON to this path.",
    )
    parser.add_argument(
        "--no-annotations",
        action="store_true",
        help="Disable GitHub Actions error annotations.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not SCHEMA_PATH.exists():
        print(f"Schema not found at {SCHEMA_PATH}", file=sys.stderr)
        return 2
    schema = load_schema()
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    to_validate, ignored = discover_files()
    if not to_validate and not ignored:
        print("No capsules found under capsules/. Nothing to validate.")
        if args.json_out:
            args.json_out.parent.mkdir(parents=True, exist_ok=True)
            args.json_out.write_text(
                json.dumps(
                    {
                        "schema": str(SCHEMA_PATH),
                        "validated": [],
                        "ignored": [],
                        "invalid_total": 0,
                    },
                    indent=2,
                )
            )
        return 0

    if ignored:
        print("Ignored files:")
        for p in ignored:
            print(f"  - {p.relative_to(ROOT)}")
        print("")

    if not to_validate:
        print(
            "No eligible *.json capsules to validate (only templates/jsonc present)."
        )
        return 0

    print(
        f"Validating {len(to_validate)} capsule(s) against schema/{SCHEMA_PATH.name} …"
    )
    invalid_total = 0
    results = []
    for path in to_validate:
        ok, messages = validate_file(validator, path)
        results.append(
            {
                "file": str(path.relative_to(ROOT)),
                "status": "ok" if ok else "error",
                "messages": messages,
            }
        )
        if ok:
            print(f"[OK]  {path.name}")
        else:
            invalid_total += 1
            print(f"[ERR] {path.name}")
            for message in messages:
                print(f"      - {message}")
            if not args.no_annotations:
                annotate_github(path, messages)

    print("\nSummary:")
    print(f"  validated: {len(to_validate)}")
    print(f"  ignored:   {len(ignored)}")
    print(f"  invalid:   {invalid_total}")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema": str(SCHEMA_PATH),
            "validated": results,
            "ignored": [str(p.relative_to(ROOT)) for p in ignored],
            "invalid_total": invalid_total,
        }
        args.json_out.write_text(json.dumps(payload, indent=2))
    if invalid_total > 0:
        print("Validation failed. See errors above.")
        return 1
    print("All capsules valid. ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
