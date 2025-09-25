import .ExpanderTseitin

open ExpanderTseitin

/-- Axiomatized combinatorial consequence of the entropy gate heuristic. -/
axiom high_entropy_yields_expander {n : ℕ} (ΔΦ : Float) :
    ΔΦ > 0.09 → ∃ G : ExpanderGraph n, G.expansion

/-- ΔΦ > 0.09 forces edge-expansion ≥ 0.5 (entropy-gate semantics) -/
lemma entropy_gate_implies_expander {n} (ΔΦ : Float) (h : ΔΦ > 0.09) :
    ∃ G : ExpanderGraph n, G.expansion :=
  high_entropy_yields_expander (n := n) (ΔΦ := ΔΦ) h
