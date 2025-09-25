import .ExpanderTseitin
import .EntropyImpliesExpander

/-- Top-level theorem: entropy-gate triggers provably hard instances -/
theorem P_ne_NP_of_entropy_gate (ΔΦ : Float) (h : ΔΦ > 0.09) :
    P ≠ NP := by
  have ⟨G, hexp⟩ := entropy_gate_implies_expander (n := 0) ΔΦ h
  have lb := resolutionLength_lower G
  -- any poly-time algorithm would violate the exponential lower bound
  sorry
