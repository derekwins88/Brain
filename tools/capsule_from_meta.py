#!/usr/bin/env python3
"""
Generate a schema-compliant capsule JSON from Day-2 sieve meta.

Usage:
  python tools/capsule_from_meta.py \
    --meta data/entropy_sieve_ci.json \
    --out  capsules/sieve-day2.json
"""
from __future__ import annotations
import argparse, json, os, sys, time
from typing import Any, Dict, List


def build_capsule(meta: Dict[str, Any], args: argparse.Namespace) -> Dict[str, Any]:
    np_hits_pct = float(meta.get("np_hits_pct", 0.0))
    np_hits = int(meta.get("np_hits", 0))
    n_traces = int(meta.get("n_traces", 0))
    csv_path = meta.get("csv_path")
    generated_at = meta.get("generated_at_utc") or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    refs: List[str] = [args.meta]
    if csv_path:
        refs.append(str(csv_path))
    refs.append("notes/index.md")

    capsule: Dict[str, Any] = {
        "id": args.capsule_id,
        "kind": "capsule",
        "title": args.title,
        "assumptions": [
            "A0: Standard complexity foundations",
            "A1: Entropy sieve heuristics approximate NP-wall detection",
        ],
        "claim": "Open capsule summarizing entropy sieve metrics (non-proof diagnostic).",
        "context": {
            "refs": refs,
            "notes": (
                f"Trace length {meta.get('trace_len')} across {n_traces} samples on {meta.get('backend')} backend. "
                f"NP hits: {np_hits} ({np_hits_pct:.2f}%). Thresholds — P: {args.p_threshold}, NP: {args.np_threshold}."
            ),
        },
        "status": args.status,
        "version": args.version,
        "created": generated_at,
        "updated": generated_at,
        "authors": [{"name": args.author}],
        "provenance": {
            "derivedFrom": [args.meta] + ([str(csv_path)] if csv_path else []),
            "tools": ["entropy-sieve", "python"],
        },
    }
    return capsule


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--meta", required=True, help="Path to sieve meta JSON")
    ap.add_argument("--out", required=True, help="Output capsule JSON path")
    ap.add_argument("--capsule-id", default="sieve-day2", help="Capsule id (kebab-case)")
    ap.add_argument("--title", default="Day-2 GPU Entropy Sieve — Summary", help="Capsule title")
    ap.add_argument("--p-threshold", type=float, default=0.045)
    ap.add_argument("--np-threshold", type=float, default=0.09)
    ap.add_argument("--status", default="draft", choices=["draft", "frozen", "superseded"], help="Capsule status field")
    ap.add_argument("--version", default="0.1.0", help="Capsule version (SemVer)")
    ap.add_argument("--author", default="Entropy Sieve Bot", help="Author name for capsule")
    args = ap.parse_args()

    with open(args.meta, encoding="utf-8") as f:
        meta = json.load(f)

    capsule = build_capsule(meta, args)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as g:
        json.dump(capsule, g, indent=2)
        g.write("\n")
    print(f"[capsule] wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
