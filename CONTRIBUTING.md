# Contributing Guide

Thanks for your interest in contributing!  
This project evolves in **Day milestones** (Day-1, Day-2, Day-3, …).  
Here’s how you can work with the current foundation.

---

## Workflow overview

- **Day-1:** Lean4 skeleton + proof-of-concept check.
- **Day-2:** Entropy sieve (`sieve.py` + `sieve.ipynb`) + CI capsule stream.
- **Day-3:** Infographic auto-render pipeline (JSON → PNG → Gallery).

---

## Running the sieve (Day-2)

Small local run (CPU is fine):

```bash
python3 sieve.py
```

Larger run (edit envs as needed):

```bash
N_TRACES=1000000 TRACE_LEN=64 CSV_PATH=data/entropy_sieve.csv python3 sieve.py
```

Capsule JSON is written under capsules/.

⸻

## Re-rendering the infographic (Day-3)

There are two ways to refresh docs/day3_infographic.png:

### Local execution

```bash
python -m nbconvert --to notebook --execute \
  notebooks/render_infographic.ipynb \
  --output /tmp/render_output.ipynb
```

This updates docs/day3_infographic.png and (optionally) docs/day3_infographic.json.

### GitHub Actions (auto)

- Push any change to main (for example, capsule JSON update).
- Workflow Auto-render infographic runs automatically:
  - Executes the notebook.
  - Validates JSON against schema.
  - Uploads PNG as artifact and/or commits it back to docs/.

⸻

## Pre-commit

This repo uses pre-commit to:

- Format Python with Black.
- Keep sieve.py and sieve.ipynb in sync via Jupytext.

Install hooks locally:

```bash
pip install pre-commit
pre-commit install
```

Then commits will run the hooks automatically.

⸻

## Submitting changes

1. Fork and branch from main.
2. Run tests:

```bash
PYTHONPATH=. pytest -q
```

3. Push and open a PR.

⸻

## Questions?

Open an issue or check the Gallery in README to see the project evolution.

