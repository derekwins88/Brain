#!/usr/bin/env python3
"""
Generate a capsule JSON from Day-2 sieve meta.

Usage:
  python tools/capsule_from_meta.py \
    --meta data/entropy_sieve_ci.json \
    --out  capsules/SIEVE_DAY2.json
"""
from __future__ import annotations
import argparse, json, os, sys, time
from typing import Any, Dict

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--meta", required=True, help="Path to sieve meta JSON")
    ap.add_argument("--out",  required=True, help="Output capsule JSON path")
    ap.add_argument("--capsule-id", default="SIEVE_DAY2", help="Capsule ID")
    ap.add_argument("--title", default="Day-2 GPU Entropy Sieve — Summary", help="Capsule title")
    ap.add_argument("--p-threshold", type=float, default=0.045)
    ap.add_argument("--np-threshold", type=float, default=0.09)
    args = ap.parse_args()

    with open(args.meta) as f:
        meta = json.load(f)

    pct = float(meta.get("np_hits_pct", 0.0))
    np_hits = int(meta.get("np_hits", 0))
    n_traces = int(meta.get("n_traces", 0))

    capsule: Dict[str, Any] = {
        "SchemaVersion": "capsule-1.1.0",
        "capsule_id": args.capsule_id,
        "title": args.title,
        "Claim": "OPEN",
        "Metadata": {
            # true iff any irreversible spikes were found in this sieve run
            "np_wall": np_hits > 0,
            # Day-2 doesn’t prove no-recovery; we’ll refine later
            "no_recovery": False,
            "sat_provenance": { "mode": "sieve", "binary": None },
        },
        "summary": {
            "np_hits_pct": round(pct, 4),
            "np_hits": np_hits,
            "n_traces": n_traces,
            "backend": meta.get("backend"),
            "trace_len": meta.get("trace_len"),
            "elapsed_sec": meta.get("elapsed_sec"),
        },
        "thresholds": {
            "P_threshold": args.p_threshold,
            "NP_threshold": args.np_threshold
        },
        "provenance": {
            "meta_path": args.meta,
            "csv_path": meta.get("csv_path"),
            "commit": os.getenv("GITHUB_SHA", None),
            "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        },
    }

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as g:
        json.dump(capsule, g, indent=2)
    print(f"[capsule] wrote {args.out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
