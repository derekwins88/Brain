# Capsules

This folder contains **capsules**: auditable, structured JSON records of
research statements. Capsules are **not proofs** — they are frozen,
versioned snapshots with context, assumptions, and provenance.

Each capsule must validate against
[`schema/capsule.schema.json`](../schema/capsule.schema.json). CI runs
`python python/validate_capsules.py` to enforce this.

## How to write a capsule

1. Copy `_template.jsonc` → `capsules/<your-id>.json`
   - Use lowercase kebab-case for the `id` (e.g. `brain-demo-0002`)
   - Bump the `version` field using [SemVer](https://semver.org/)
2. Fill in the required fields:
   - `id`, `kind` (must be `"capsule"`), `title`, `assumptions[]`,
     `claim`, `context.refs[]`, `status`, `version`, `created`
3. Update `authors` with your name/email/ORCID (at least `name`)
4. Commit + push. CI will validate automatically.

## Local validation

```bash
python -m pip install -U jsonschema rfc3339-validator
python python/validate_capsules.py
```

## Status lifecycle
- `draft`: still evolving
- `frozen`: fixed snapshot (no changes except metadata)
- `superseded`: replaced by another capsule (see `provenance.derivedFrom`)

## Example
See [`brain-demo-0001.json`](brain-demo-0001.json) for a minimal valid capsule.

---

💡 Tip: keep `invalid-example.json` around locally to test validation,
but don’t commit it if you want green CI.
