# Capsule Format

```json
{
  "id": "cap-2025-09-24-entropy-gate",
  "version": 1,
  "claim": "For corpus X, Gate G separates P-regime/NP-regime with threshold τ.",
  "assumptions": ["A1", "A2"],
  "evidence": ["link-to-docs", "hash:sha256:..."],
  "status": "draft",
  "created_at": "2025-09-24T00:00:00Z"
}
```

Conventions

- Keep claims testable or at least falsifiable.
- Reference artifacts with stable hashes (sha256).
- Prefer small capsules over mega-essays. Your future self will thank you.
