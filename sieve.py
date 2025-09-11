#!/usr/bin/env python3
"""
Day-2: GPU Entropy Sieve
- Generates/streams entropy traces and flags irreversible spikes (ΔΦ > NP_THRESHOLD)
- Uses CuPy (GPU) if available; falls back to NumPy (CPU)
- Writes summary CSV + meta JSON under ./data/
"""
from __future__ import annotations
import os, sys, time, math, csv, json, random
from typing import Tuple

# Prefer GPU via CuPy; fall back to NumPy
backend = "cpu"
try:
    import cupy as cp  # type: ignore
    _ = cp.cuda.runtime.getDeviceCount()
    xp = cp
    backend = "cuda"
except Exception:
    import numpy as np
    xp = np
    backend = "cpu"

# Config via env (small defaults for CI)
NP_THRESHOLD = float(os.getenv("NP_THRESHOLD", "0.09"))
P_THRESHOLD  = float(os.getenv("P_THRESHOLD",  "0.045"))
N_TRACES     = int(os.getenv("N_TRACES",      "20000"))
TRACE_LEN    = int(os.getenv("TRACE_LEN",     "48"))
SEED         = int(os.getenv("SEED",          "42"))
CSV_PATH     = os.getenv("CSV_PATH", "data/entropy_sieve_ci.csv")
META_PATH    = os.getenv("META_PATH", "data/entropy_sieve_ci.json")
BATCH        = int(os.getenv("BATCH",         "100000"))

SPIKE_PROB   = float(os.getenv("SPIKE_PROB", "0.035"))
NOISE_SIGMA  = float(os.getenv("NOISE_SIGMA","0.02"))

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
    base = 0.03 + 0.03 * rng_rand((n, 1))          # [0.03, 0.06)
    noise = rng_normal((n, length), NOISE_SIGMA)
    traces = xp.clip(base + noise.cumsum(axis=1)/length, 0, None)

    # Inject spike near last third
    spikes = (rng_rand((n, 1)) < SPIKE_PROB).astype(traces.dtype)
    spike_height = NP_THRESHOLD + 0.02 + 0.05 * rng_rand((n, 1))
    idx = xp.full((n,), int(0.66 * length))
    rows = xp.arange(n, dtype=xp.int32) if backend == "cuda" else xp.arange(n)
    traces[rows, idx] += (spikes[:, 0] * spike_height[:, 0])
    return traces

def ensure_dir(path: str):
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)

def main():
    t0 = time.time()
    random.seed(SEED)
    ensure_dir(CSV_PATH); ensure_dir(META_PATH)

    total = 0
    total_np = 0
    batches = math.ceil(N_TRACES / BATCH)

    with open(CSV_PATH, "w", newline="") as fcsv:
        w = csv.writer(fcsv)
        w.writerow(["trace_id", "max_delta_phi", "np_hit", "length", "backend"])

        for _ in range(batches):
            size = min(BATCH, N_TRACES - total)
            traces = gen_traces(size, TRACE_LEN)
            maxvals = traces.max(axis=1)
            np_hits = (maxvals > NP_THRESHOLD)

            if backend == "cuda":
                maxvals_np = xp.asnumpy(maxvals)
                np_hits_np = xp.asnumpy(np_hits.astype(xp.int32))
            else:
                maxvals_np = maxvals
                np_hits_np = np_hits.astype(int)

            for i in range(size):
                w.writerow([total + i, float(maxvals_np[i]), int(np_hits_np[i]), TRACE_LEN, backend])

            total += size
            total_np += int(np_hits_np.sum())

            if backend == "cuda":
                del traces, maxvals, np_hits
                xp.get_default_memory_pool().free_all_blocks()

    pct = (100.0 * total_np / total) if total else 0.0
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
