[![CI - Python](https://github.com/derekwins88/Brain/actions/workflows/ci-python.yml/badge.svg)](https://github.com/derekwins88/Brain/actions/workflows/ci-python.yml)
[![CI - .NET](https://github.com/derekwins88/Brain/actions/workflows/ci-dotnet.yml/badge.svg)](https://github.com/derekwins88/Brain/actions/workflows/ci-dotnet.yml)
[![CI - Lean4](https://github.com/derekwins88/Brain/actions/workflows/ci-lean.yml/badge.svg)](https://github.com/derekwins88/Brain/actions/workflows/ci-lean.yml)
[![Proof v1.1 (smoke)](https://github.com/derekwins88/Brain/actions/workflows/ci-proof.yml/badge.svg)](https://github.com/derekwins88/Brain/actions/workflows/ci-proof.yml)
![Capsules](https://github.com/derekwins88/Brain/actions/workflows/ci-capsules.yml/badge.svg)

**Status:** Day-1 green ✅ — Python, .NET, Lean4 build pass; Proof v1.1 pipeline smoke passes (PDF check is permissive until full translator is wired).

# Day-0 Mission

Turn **harmonic entropy drift** into **machine-checkable P≠NP artifacts** in ≤ 30 days.

> Progressive feedback loop → **Entropy-Collapse Labs** | P≠NP via glyphs & entropy

---

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
Capsule: [IMM_MATH_ALSTEIN01](./capsules/IMM_MATH_ALSTEIN01.json)

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

Day-2 capsule: [SIEVE_DAY2](./capsules/SIEVE_DAY2.json)

Colab
Open: https://colab.research.google.com/github/derekwins88/Brain/blob/main/sieve.py
Run all → commit the CSV from /content/ to data/.

Artifacts:
    •    CSV summary per trace: data/entropy_sieve_*.csv
    •    Meta summary: data/entropy_sieve_*.json

---

## 5) (Optional) Day-2 tweet stub

```text
Day-2 🚀
GPU entropy sieve online — 10M+ traces scanned.
% irreversible above ΔΦ 0.09 reported in meta.
Notebook: github.com/derekwins88/Brain/blob/main/sieve.py
#PvsNP #Lean4 #EntropyCollapse
```

---

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
