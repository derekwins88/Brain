#!/usr/bin/env python3
"""
Day-2: GPU Entropy Sieve
- Generates/streams entropy traces and flags irreversible spikes (ΔΦ > NP_threshold)
- Uses CuPy (GPU) if available; falls back to NumPy (CPU)
- Writes summary CSV(s) under ./data/
"""

from __future__ import annotations
import os, sys, time, math, csv, json, random
from typing import Tuple

# --- Try GPU (CuPy), else CPU (NumPy) ---------------------------------------
xp = None
backend = "cpu"
try:
    import cupy as cp  # type: ignore
    # Ensure at least a device is visible
    _ = cp.cuda.runtime.getDeviceCount()
    xp = cp
    backend = "cuda"
except Exception:
    import numpy as np
    xp = np
    backend = "cpu"

# --- Config -----------------------------------------------------------------
NP_THRESHOLD = float(os.getenv("NP_THRESHOLD", "0.09"))    # irreversible ΔΦ
P_THRESHOLD  = float(os.getenv("P_THRESHOLD",  "0.045"))   # soft/linear bound
N_TRACES     = int(os.getenv("N_TRACES",      "1000000"))  # 1e6 default for CI; bump to 1e8 on Colab
TRACE_LEN    = int(os.getenv("TRACE_LEN",     "64"))       # samples per trace
SEED         = int(os.getenv("SEED",          "42"))
CSV_PATH     = os.getenv("CSV_PATH", "data/entropy_sieve_sample.csv")
META_PATH    = os.getenv("META_PATH", "data/entropy_sieve_meta.json")
BATCH        = int(os.getenv("BATCH",         "100000"))   # process in chunks

# Synthetic generator controls (kept simple for Day-2 demo)
SPIKE_PROB   = float(os.getenv("SPIKE_PROB", "0.035"))     # ~3.5% with spikes > 0.09
NOISE_SIGMA  = float(os.getenv("NOISE_SIGMA","0.02"))

# --- Helpers ----------------------------------------------------------------
def rng_rand(shape, seed=None):
    if backend == "cuda":
        rs = xp.random.RandomState(SEED if seed is None else seed)
        return rs.rand(*shape)
    else:
        rs = xp.random.default_rng(SEED if seed is None else seed)
        return rs.random(shape)

def rng_normal(shape, sigma, seed=None):
    if backend == "cuda":
        rs = xp.random.RandomState(SEED if seed is None else seed)
        return rs.normal(loc=0.0, scale=sigma, size=shape)
    else:
        rs = xp.random.default_rng(SEED if seed is None else seed)
        return rs.normal(loc=0.0, scale=sigma, size=shape)

def gen_traces(n: int, length: int) -> xp.ndarray:
    """
    Generate entropy drift traces with occasional irreversible spikes.
    Baseline noise around ~0.03–0.06; spikes push ΔΦ > NP_THRESHOLD.
    """
    base = 0.03 + 0.03 * rng_rand((n, 1))                     # [0.03, 0.06)
    noise = rng_normal((n, length), NOISE_SIGMA)              # zero-mean
    traces = xp.clip(base + noise.cumsum(axis=1)/length, 0, None)

    # Inject spikes
    spikes = (rng_rand((n, 1)) < SPIKE_PROB).astype(traces.dtype)
    spike_height = NP_THRESHOLD + 0.02 + 0.05 * rng_rand((n, 1))  # > NP_THRESHOLD
    # Put spike near last third of the trace
    idx = xp.full((n,), int(0.66 * length))
    if backend == "cuda":
        rows = xp.arange(n, dtype=xp.int32)
        traces[rows, idx] += (spikes[:, 0] * spike_height[:, 0])
    else:
        rows = xp.arange(n)
        traces[rows, idx] += (spikes[:, 0] * spike_height[:, 0])
    return traces

def stats_from_traces(traces: xp.ndarray) -> Tuple[int, int, float]:
    n = traces.shape[0]
    maxvals = traces.max(axis=1)
    np_hits = (maxvals > NP_THRESHOLD)
    count_np = int(xp.asnumpy(np_hits).sum()) if backend == "cuda" else int(np_hits.sum())
    pct = (100.0 * count_np / n) if n else 0.0
    return n, count_np, pct

def ensure_dir(path: str):
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)

# --- Main -------------------------------------------------------------------
def main():
    t0 = time.time()
    random.seed(SEED)

    ensure_dir(CSV_PATH)
    ensure_dir(META_PATH)

    total = 0
    total_np = 0
    batches = math.ceil(N_TRACES / BATCH)

    # Write CSV header
    with open(CSV_PATH, "w", newline="") as fcsv:
        w = csv.writer(fcsv)
        w.writerow(["trace_id", "max_delta_phi", "np_hit", "length", "backend"])

        for b in range(batches):
            size = min(BATCH, N_TRACES - total)
            traces = gen_traces(size, TRACE_LEN)
            # Compute metrics
            maxvals = traces.max(axis=1)
            np_hits = (maxvals > NP_THRESHOLD)

            if backend == "cuda":
                maxvals_np = xp.asnumpy(maxvals)
                np_hits_np = xp.asnumpy(np_hits.astype(xp.int32))
            else:
                maxvals_np = maxvals
                np_hits_np = np_hits.astype(int)

            # Emit CSV rows (only summary per trace for Day-2)
            for i in range(size):
                w.writerow([total + i, float(maxvals_np[i]), int(np_hits_np[i]), TRACE_LEN, backend])

            # update totals
            total += size
            total_np += int(np_hits_np.sum())

            # free GPU memory between batches
            if backend == "cuda":
                del traces, maxvals, np_hits
                xp.get_default_memory_pool().free_all_blocks()

    pct = 100.0 * total_np / total if total else 0.0

    # Write meta JSON
    meta = {
        "SchemaVersion": "sieve-1.0.0",
        "backend": backend,
        "n_traces": total,
        "trace_len": TRACE_LEN,
        "np_threshold": NP_THRESHOLD,
        "p_threshold": P_THRESHOLD,
        "spike_prob": SPIKE_PROB,
        "noise_sigma": NOISE_SIGMA,
        "np_hits": total_np,
        "np_hits_pct": pct,
        "csv_path": CSV_PATH,
        "elapsed_sec": round(time.time() - t0, 3)
    }
    with open(META_PATH, "w") as f:
        json.dump(meta, f, indent=2)

    print(f"[sieve] backend={backend} traces={total} np_hits={total_np} ({pct:.2f}%) csv={CSV_PATH}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
