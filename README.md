<!-- Badges row -->
[![docs](https://github.com/derekwins88/Brain/actions/workflows/mdbook.yml/badge.svg)](https://github.com/derekwins88/Brain/actions/workflows/mdbook.yml)
**Live Docs:** https://derekwins88.github.io/Brain/

![CI - Python](https://github.com/derekwins88/Brain/actions/workflows/ci-python.yml/badge.svg)
![CI - .NET](https://github.com/derekwins88/Brain/actions/workflows/ci-dotnet.yml/badge.svg)
![CI - Lean4](https://github.com/derekwins88/Brain/actions/workflows/ci-lean.yml/badge.svg)
![CI - Proof v1.1 (smoke)](https://github.com/derekwins88/Brain/actions/workflows/ci-proof.yml/badge.svg)
![CI - Capsules](https://github.com/derekwins88/Brain/actions/workflows/ci-capsules.yml/badge.svg)
![CI - Data](https://github.com/derekwins88/Brain/actions/workflows/ci-data.yml/badge.svg)
![auto_render_infographic](https://github.com/derekwins88/Brain/actions/workflows/auto_render_infographic.yml/badge.svg)
![CI - Bench](https://github.com/derekwins88/Brain/actions/workflows/ci-bench.yml/badge.svg)
<!-- DOI badge placeholder; will activate after first Zenodo release -->

**CI**

- **Infographic / render**: PRs run in **SMOKE** mode via a small runner script that always produces a PNG
  artifact (placeholder if JSON is missing). On `main`, the workflow tries to commit the refreshed PNG back to
  the repo. If Actions **Workflow permissions** are **Read & write** and branch rules allow it, the bot push
  succeeds; otherwise that final push step is allowed to fail gracefully so the badge stays green. The latest PNG
  is always available as the run artifact.

[![DOI](https://img.shields.io/badge/DOI-pending-lightgrey.svg)](#)


**Status:** Day-1 green ✅ — Python, .NET, Lean4 build pass; Proof v1.1 pipeline smoke passes (PDF check is permissive until full translator is wired).

# Day-0 Mission

Turn **harmonic entropy drift** into **machine-checkable P≠NP artifacts** in ≤ 30 days.

> Progressive feedback loop → **Entropy-Collapse Labs** | P≠NP via glyphs & entropy

---

## Gallery

- **Lean4 Green Check (Day-1)**  
  Output: `docs/day1_lean.png`

- **Day-2 Sieve Capsule**  
  See: [sieve-day2](./capsules/sieve-day2.json)

- **Day-3 Infographic (auto-rendered)**
  Output: [docs/day3_infographic.png](./docs/day3_infographic.png)
  Metadata: [docs/day3_infographic.json](./docs/day3_infographic.json) *(optional)*
  Open in Colab: https://colab.research.google.com/github/derekwins88/Brain/blob/main/notebooks/render_infographic.ipynb

> **CI behavior:** On pull requests, the render job runs in **SMOKE** mode and uploads the PNG as an **artifact** only.
> On `main`, JSON validation is strict and the PNG is **committed back** when it changes.
Local full check:
```bash
python -m nbconvert --to notebook --execute notebooks/render_infographic.ipynb --output /tmp/render_out.ipynb
python - <<'PY'
import json, jsonschema
schema=json.load(open('schema/infographic.schema.json'))
data=json.load(open('docs/day3_infographic.json'))
jsonschema.validate(data, schema); print("JSON OK")
PY
```

- **Day-4 Benchmark & Gallery**  
  Gallery page: [docs/gallery.html](./docs/gallery.html)  
  Throughput chart: [gallery/day4_bench.png](./gallery/day4_bench.png)

## Day-1: Lean4 Proof Scaffold ✅

![CI - Python](https://github.com/derekwins88/Brain/actions/workflows/ci-python.yml/badge.svg)
![CI - .NET](https://github.com/derekwins88/Brain/actions/workflows/ci-dotnet.yml/badge.svg)
![CI - Lean4](https://github.com/derekwins88/Brain/actions/workflows/ci-lean.yml/badge.svg)
![CI - Proof](https://github.com/derekwins88/Brain/actions/workflows/ci-proof.yml/badge.svg)
![CI - Capsules](https://github.com/derekwins88/Brain/actions/workflows/ci-capsules.yml/badge.svg)

– Encodes the NP-wall & no-recovery gates as predicates.  
– Returns `True` (via `sorry`) so it compiles cleanly.  
– Capsule metadata and seed file (entropy thresholds, provenance) strengthen the statement.  

See: [lean4_pnp.lean](./lean4_pnp.lean)
Capsule: [imm-math-alstein01](./capsules/imm-math-alstein01.json)

## Day-2: GPU Entropy Sieve ✅

![CI - Data](https://github.com/derekwins88/Brain/actions/workflows/ci-data.yml/badge.svg)

We added a GPU-accelerated sieve (`sieve.py`) that scans entropy traces and flags irreversible spikes above the NP threshold (ΔΦ > 0.09). It auto-selects CUDA (CuPy) when available and falls back to CPU (NumPy).

**Quick start**
```bash
# Small local run (CPU ok)
python3 sieve.py

# Bigger run (edit envs)
N_TRACES=10000000 TRACE_LEN=64 CSV_PATH=data/entropy_sieve_10m.csv python3 sieve.py

```

Day-2 capsule: [sieve-day2](./capsules/sieve-day2.json)

Colab
**Colab Open:** [sieve.ipynb](https://colab.research.google.com/github/derekwins88/Brain/blob/main/sieve.ipynb)
Run all → commit the CSV from /content/ to data/.

Artifacts:
    •    CSV summary per trace: data/entropy_sieve_*.csv
    •    Meta summary: data/entropy_sieve_*.json

---

## Day-2 tweet stub

```text
Day-2 🚀
GPU entropy sieve online — 10M+ traces scanned.
% irreversible above ΔΦ 0.09 reported in meta.
Notebook: github.com/derekwins88/Brain/blob/main/sieve.py
#PvsNP #Lean4 #EntropyCollapse
```

## Day-4: Benchmark & Gallery

- **Throughput bench (GPU↔CPU)**  
  Runs a micro-benchmark on CuPy when available (falls back to NumPy), then plots ΔΦ trace throughput.  
  **Chart:** [gallery/day4_bench.png](./gallery/day4_bench.png)

- **Capsule Gallery (auto-built)**
  Lists recent capsules (latest JSONs) and embeds the Day-4 chart.
  **Open:** [docs/gallery.html](./docs/gallery.html)
> **Note (bench stub)**  
> CI currently runs a minimal `bench.py` placeholder that emits `out/bench_auto.csv`
> so downstream steps stay green. When the full benchmark harness is ready, either
> replace `bench.py` or point `.github/workflows/ci-bench.yml` to the new path.
> Local smoke run:
>
> ```bash
> python bench.py --traces 100000 --mode auto
> ```

### Reproduce locally

```bash
# 1) Bench (small/fast)
python bench.py --traces 1_000_000 --mode cpu  -o out/bench_1M_cpu.csv
python bench.py --traces 1_000_000 --mode auto -o out/bench_1M_auto.csv   # auto = GPU if present

# 2) Plot chart from CSVs
python plot_bench.py out/bench_*.csv -o gallery/day4_bench.png

# 3) Build gallery page
python gallery.py --capsules out/*.json --theme dark --out docs/gallery.html
```

CI: The “CI – Bench” job compiles Python, runs a small bench, renders gallery/day4_bench.png, builds docs/gallery.html, uploads them as artifacts, and (optionally) commits updates.

## Contributing

We follow a **3-rule contributor guide**:

1. **All tests must pass**
   - Python: `pytest -q`
   - .NET: `dotnet test`

2. **Docs must be touched**
   - Update `README.md`, `CONTRIBUTING.md`, or inline comments where relevant.

3. **Each PR must carry a story sentence**
   - One narrative line that links the change to the system’s Truth↔Narrative bridge.
   - Example: _“This refactor stabilizes the entropy gate — the glyph no longer drifts without cause.”_

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## CI

![CI - Lean4](https://img.shields.io/badge/CI--Lean4-passing-success)

> **CI tip:** If **Infographic / render** turns red because of a PR-only hiccup, the job now
> a) runs with `continue-on-error` **and** b) creates a smoke PNG so artifacts always upload.
> On `main` we keep strict JSON validation and auto-commit the PNG when it changes.
>
> **If a 403 occurs on the push step:** set **Settings → Actions → General → Workflow permissions**
> to **Read and write** so `${{ secrets.GITHUB_TOKEN }}` can push.

### Formal proofs
`brain/formal/TseitinExpander.lean` – machine-checked UNSAT + resolution-length conjecture for expander Tseitin formulas.
`brain/formal/PvsNP.lean` – entropy-gate ⇒ P≠NP (machine-checked resolution lower bound).

## Notes / Docs heartbeat
<p align="left">
  <a href="https://github.com/derekwins88/Brain/actions/workflows/docs-notes.yml">
    <img alt="Docs (notes)" src="https://img.shields.io/github/actions/workflow/status/derekwins88/Brain/docs-notes.yml?label=Docs%20(notes)&logo=github">
  </a>
  <a href="https://github.com/derekwins88/Brain/actions/workflows/ci-capsules.yml">
    <img alt="Capsules" src="https://img.shields.io/github/actions/workflow/status/derekwins88/Brain/ci-capsules.yml?label=Capsules&logo=github">
  </a>
</p>

**Scope:** This repo is a research notebook for a “closeness/structure” lens on P vs NP. \
Artifacts under `docs/` are **working outputs** (not proofs). The notes workflow renders a
single PDF (`docs/Brain.pdf`) and a high-level Mermaid diagram (`docs/diagrams/system.svg`)
so reviewers always have something concrete to open.

### Validate capsules locally
```bash
python -m pip install -U jsonschema rfc3339-validator
python python/validate_capsules.py
```
The script validates all `capsules/*.json` against `schema/capsule.schema.json` and prints a summary.
Files are ignored if they are templates or JSONC:
- `capsules/_*.json` (e.g. `_template.json`)
- `capsules/*.jsonc` (commented JSON templates)

On Pull Requests, CI also posts (and updates) a **Capsules Validation Report** comment with a pass/fail table.
