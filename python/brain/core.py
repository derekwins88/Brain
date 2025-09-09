from math import isfinite


def entropy_delta(series: list[float]) -> float:
    """Toy placeholder: normalized spread in [0,1]. Ignores non-finite values."""
    clean = [x for x in series or [] if isinstance(x, (int, float)) and isfinite(x)]
    if len(clean) < 2:
        return 0.0
    lo, hi = min(clean), max(clean)
    if hi == lo:
        return 0.0
    denom = max(abs(hi), 1e-9)
    return (hi - lo) / denom
