import .LPSExpander
import .ExpanderTseitin

open LPSExpander ExpanderTseitin

/-- Closed-form entropy drift for LPS-Tseitin formulas -/
lemma entropy_LPS (n : ℕ) (hn : ∃ p, Nat.Prime p ∧ p % 4 = 1 ∧ n = p + 1 ∧ p ≥ 17) :
    ΔΦ (tseitinCnf (explicitExpander n hn)) > 0.09 := by
  -- compute clause/variable ratio and apply the curvature lemma
  have ratio := LPS.clause_variable_ratio n hn
  have curvature := entropy_curvature ratio
  linarith
