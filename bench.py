#!/usr/bin/env python3
"""
bench.py — placeholder micro-benchmark

Purpose
-------
Keeps CI green by producing a deterministic CSV artifact that downstream
steps (plot, gallery) can consume. Replace with the real harness later.

Usage (examples)
----------------
python bench.py --traces 100000 --mode auto
python bench.py --traces 1e6 --mode gpu --out out/bench_1M_gpu.csv
"""

from __future__ import annotations
import argparse, os, csv, time, math

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--traces", type=float, default=100_000,
                    help="Number of traces (accepts float for scientific notation).")
    ap.add_argument("--mode", choices=["auto", "cpu", "gpu"], default="auto",
                    help="Execution mode hint.")
    ap.add_argument("--out", default="out/bench_auto.csv",
                    help="Output CSV path.")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)

    # Deterministic “fake” timing that scales with trace count,
    # just to produce sensible numbers for charts.
    traces = float(args.traces)
    base_tps = 125_000.0
    mode_factor = {"cpu": 0.8, "gpu": 8.0, "auto": 1.0}[args.mode]
    tps = base_tps * mode_factor
    elapsed = traces / tps if tps > 0 else 0.0

    now = int(time.time())
    with open(args.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "mode", "traces", "throughput_traces_per_s", "elapsed_s"])
        w.writerow([now, args.mode, int(traces), f"{tps:.3f}", f"{elapsed:.6f}"])

    print(f"[bench] wrote CSV → {args.out}")
    print(f"[bench] mode={args.mode} traces={int(traces)} tps≈{tps:.0f} elapsed≈{elapsed:.3f}s")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
