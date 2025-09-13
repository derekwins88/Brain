# GLYPH⇌TRADER⇌ENGINE — Unified Symbolic Engine (foundational stub)
# Dependency-free, deterministic; OK for CI and quick demos.

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import List, Dict, Tuple, Any
import hashlib
import json
import datetime as dt


# ----------------------------
# Core data structures
# ----------------------------


@dataclass(frozen=True)
class Glyph:
    symbol: str
    entropy: float
    narrative_tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "entropy": self.entropy,
            "narrative_tags": list(self.narrative_tags),
        }


@dataclass(frozen=True)
class Capsule:
    capsule_id: str
    timestamp: str
    proof_claim: str  # "P≠NP", "OPEN", "Contradiction"
    financial_forecast: Dict[str, Any]
    ethical_audit: Dict[str, Any]
    fork_paths: List[Dict[str, Any]]
    raw_inputs: Dict[str, Any]

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)


# ----------------------------
# Translator ⇌ Proof ⇌ Core
# ----------------------------


class TranslatorCore:
    """
    Very small, deterministic stand-in for your TranslatorCoreBatchRunner.
    - Motifs → toy CNF clauses
    - MiniSatBridge.solve → detects obvious contradiction A & ¬A
    - Claim logic:
        * If contradiction → "Contradiction"
        * Else if NP-wall motif present (⥁ + ⚛) → "P≠NP"
        * Else → "OPEN"
    """

    def motif_to_clauses(self, motifs: List[str]) -> List[List[str]]:
        # Toy CNF encoder: each motif becomes a single-literal clause;
        # special strings with "NOT:" become negated literals.
        clauses: List[List[str]] = []
        for m in motifs:
            m = m.strip()
            if not m:
                continue
            if m.startswith("NOT:"):
                clauses.append([f"¬{m[4:]}"])
            else:
                clauses.append([m])
        return clauses

    def minisat_solve(self, cnf: List[List[str]]) -> bool:
        # Detect immediate contradiction: literal X and ¬X appear as unit clauses.
        lits = {c[0] for c in cnf if c}
        for lit in list(lits):
            if lit.startswith("¬") and lit[1:] in lits:
                return False  # UNSAT
            if f"¬{lit}" in lits:
                return False
        return True  # SAT (toy)

    def run_proof_batch(self, motifs: List[str]) -> Tuple[Dict[str, Any], List[Glyph]]:
        cnf = self.motif_to_clauses(motifs)
        sat = self.minisat_solve(cnf)

        # Determine claim
        flat = " ".join(motifs)
        has_np_wall = ("⥁" in flat) and ("⚛" in flat)
        claim = "Contradiction" if not sat else ("P≠NP" if has_np_wall else "OPEN")

        # Emit glyphs: pass through motifs as glyphs with simple entropy
        glyphs: List[Glyph] = []
        for m in motifs:
            if not m:
                continue
            sym = m.replace("NOT:", "¬")
            entropy = (
                0.12 if sym in ("⥁", "⚛") else (0.05 if sym.startswith("¬") else 0.08)
            )
            tags = ["proof-out"]
            if sym in ("⥁", "⚛"):
                tags.append("np-wall-signal")
            glyphs.append(Glyph(symbol=sym, entropy=entropy, narrative_tags=tags))

        results = {
            "sat": sat,
            "claim": claim,
            "clauses": cnf,
        }
        return results, glyphs


# ----------------------------
# GLYPH ⇌ TRADER ⇌ ENGINE
# ----------------------------


class TraderEngine:
    """
    Simplified market forecaster & action engine.
    Rule: if {⥁, ⚛} detected in inputs → predict collapse with high confidence,
          else neutral drift.
    Produces a new "☑" collapse glyph when a collapse signal is seen.
    """

    COLLAPSE_GLYPH = "☑"

    def forecast_and_act(
        self, input_glyphs: List[Glyph]
    ) -> Tuple[Dict[str, Any], List[Glyph]]:
        syms = {g.symbol for g in input_glyphs}
        if {"⥁", "⚛"} <= syms:
            forecast = {
                "action": "hedge",
                "market": "SPY",
                "confidence": 0.93,
                "thesis": "entropy-collapse",
            }
            new = [
                Glyph(
                    symbol=self.COLLAPSE_GLYPH,
                    entropy=0.15,
                    narrative_tags=["collapse", "hedge-signal"],
                )
            ]
        else:
            forecast = {
                "action": "hold",
                "market": "SPY",
                "confidence": 0.55,
                "thesis": "neutral",
            }
            new = []
        return forecast, new

    def export_crystal_patterns(self, high_gain_glyphs: List[Glyph]) -> List[str]:
        # If collapse glyph present, emit a motif that feeds back to the translator
        if any(g.symbol == self.COLLAPSE_GLYPH for g in high_gain_glyphs):
            return ["CRYSTAL:COLLAPSE☑"]
        return []


# ----------------------------
# IMM ⇌ TRANSLATE ⇌ GLYPH-MUTATION (Ethical audit)
# ----------------------------


class GlyphMutator:
    """
    EthicalBound validator (simplified).
    Warns on high-confidence 'buy' with no entropic confirmation (⥁ missing).
    """

    def audit_narrative(
        self, forecast: Dict[str, Any], initial_glyphs: List[Glyph]
    ) -> Dict[str, Any]:
        syms = {g.symbol for g in initial_glyphs}
        if (
            forecast.get("action") == "buy"
            and forecast.get("confidence", 0) > 0.9
            and "⥁" not in syms
        ):
            return {
                "status": "Warning",
                "reason": "High-confidence buy without entropic (⥁) confirmation",
            }
        return {"status": "Harmonic", "reason": "Audit passed"}


# ----------------------------
# ParadoxForker
# ----------------------------


class ParadoxForker:
    """
    When a contradiction appears, fork new clause paths (creative exploration).
    """

    def detect_and_fork(
        self, proof_claim: str, input_clauses: List[List[str]]
    ) -> List[Dict[str, Any]]:
        if proof_claim != "Contradiction":
            return []
        forks: List[Dict[str, Any]] = []
        # Create two deterministic forks: flip first literal, and add constraint
        base = [c[:] for c in input_clauses]
        if base:
            first = base[0][0]
            flipped = f"¬{first}" if not first.startswith("¬") else first[1:]
            fork1 = [
                {
                    "clauses": [[flipped] if i == 0 else c for i, c in enumerate(base)],
                    "HarmonicViable": True,
                }
            ]
            forks.extend(fork1)
        fork2 = [{"clauses": base + [["STABILIZE"]], "HarmonicViable": False}]
        forks.extend(fork2)
        return forks


# ----------------------------
# Orchestrator
# ----------------------------


class UnifiedEngine:
    def __init__(self) -> None:
        self.translator = TranslatorCore()
        self.trader = TraderEngine()
        self.mutator = GlyphMutator()
        self.forker = ParadoxForker()

    def _utc_now(self) -> str:
        return (
            dt.datetime.now(dt.timezone.utc)
            .isoformat(timespec="seconds")
            .replace("+00:00", "Z")
        )

    def _capsule_id(self, payload: Dict[str, Any]) -> str:
        blob = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
        return hashlib.sha256(blob).hexdigest()

    def run_engine(self, motifs: List[str]) -> Capsule:
        # 1) Translator core
        proof_results, initial_glyphs = self.translator.run_proof_batch(motifs)

        # 2) Fork on contradiction
        forks = self.forker.detect_and_fork(
            proof_results["claim"], proof_results["clauses"]
        )

        # 3) Forecast & act
        forecast, new_glyphs = self.trader.forecast_and_act(initial_glyphs)

        # 4) Ethical audit
        audit = self.mutator.audit_narrative(forecast, initial_glyphs)

        # 5) Export crystal patterns (feedback)
        feedback_motifs = self.trader.export_crystal_patterns(new_glyphs)
        if feedback_motifs:
            # (For now, we only surface the opportunity; you can loop this externally.)
            print(f"[feedback] New motifs available for refinement: {feedback_motifs}")

        # 6) Assemble capsule
        raw_inputs = {
            "motifs": motifs,
            "proof_results": proof_results,
            "forecast": forecast,
            "feedback_motifs": feedback_motifs,
        }
        capsule_payload = {
            "timestamp": self._utc_now(),
            "proof_claim": proof_results["claim"],
            "financial_forecast": forecast,
            "ethical_audit": audit,
            "fork_paths": forks,
            "raw_inputs": raw_inputs,
        }
        cid = self._capsule_id(capsule_payload)

        return Capsule(
            capsule_id=cid,
            timestamp=capsule_payload["timestamp"],
            proof_claim=capsule_payload["proof_claim"],
            financial_forecast=capsule_payload["financial_forecast"],
            ethical_audit=capsule_payload["ethical_audit"],
            fork_paths=capsule_payload["fork_paths"],
            raw_inputs=capsule_payload["raw_inputs"],
        )


# ----------------------------
# Quick demo (can be removed in CI)
# ----------------------------


if __name__ == "__main__":
    engine = UnifiedEngine()
    # Example 1: NP-wall signal present (⥁ + ⚛)
    motifs = ["⥁", "⚛", "MARKET:SPY"]
    cap = engine.run_engine(motifs)
    print(cap.to_json())

    # Example 2: explicit contradiction via unit pair A & ¬A
    motifs_contradiction = ["A", "NOT:A", "MARKET:QQQ"]
    cap2 = engine.run_engine(motifs_contradiction)
    print(cap2.to_json())
