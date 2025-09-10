# Lean4 scaffold (Day-1)

## Build locally
```bash
cd lean
lake update   # fetch mathlib
lake build
```

Notes
- Brain/EntropyWall.lean contains a safe placeholder theorem with goal True so CI stays green.
- If you want a sorry-based skeleton (e.g., for SAT reductions), put it in a separate file or keep CI permissive.
