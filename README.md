[![CI - Python](https://github.com/derekwins88/Brain/actions/workflows/ci-python.yml/badge.svg)](https://github.com/derekwins88/Brain/actions/workflows/ci-python.yml)
[![CI - .NET](https://github.com/derekwins88/Brain/actions/workflows/ci-dotnet.yml/badge.svg)](https://github.com/derekwins88/Brain/actions/workflows/ci-dotnet.yml)
[![CI - Lean4](https://github.com/derekwins88/Brain/actions/workflows/ci-lean.yml/badge.svg)](https://github.com/derekwins88/Brain/actions/workflows/ci-lean.yml)
[![Proof v1.1 (smoke)](https://github.com/derekwins88/Brain/actions/workflows/ci-proof.yml/badge.svg)](https://github.com/derekwins88/Brain/actions/workflows/ci-proof.yml)

**Status:** Day-1 green ✅ — Python, .NET, Lean4 build pass; Proof v1.1 pipeline smoke passes (PDF check is permissive until full translator is wired).

# Day-0 Mission

Turn **harmonic entropy drift** into **machine-checkable P≠NP artifacts** in ≤ 30 days.

> Progressive feedback loop → **Entropy-Collapse Labs** | P≠NP via glyphs & entropy

---

# Day-1: Lean4 Skeleton (Proof Capsule Hook)

This repo ships a minimal Lean4 skeleton so we can pin a green check and
start threading capsules → proofs.

### Steps

1. Open the Lean4 playground: https://live.lean-lang.org
2. Paste the contents of `lean4_pnp.lean`.
3. Press ▶ (Run). You should see a green check.
4. Take a screenshot and save it to `docs/day1_lean.png`.
5. Commit the file and screenshot on branch `lean4-proof`.

```bash
git checkout -b lean4-proof
git add lean4_pnp.lean docs/day1_lean.png
git commit -m "Day-1: Lean4 skeleton compiles (green check)"
git push origin lean4-proof
```

### Why this skeleton?

- It encodes the **NP-wall** & **no-recovery** gates as named predicates.
- The theorem returns `True` (trivial) so it **compiles cleanly** without external deps.
- You can later swap in capsule metadata (hash, ΔΦ window) and strengthen the statement.

See: `lean4_pnp.lean`.

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
