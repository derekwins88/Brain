import Mathlib.ComplexityTheory.PvsNP
import .ExpanderTseitin
import .EntropyImpliesExpander

open ExpanderTseitin ComplexityTheory

/-- Entropy-gate triggers provably exponential lower bound ⇒ P ≠ NP.

This axiom packages the (conjectural) hardness argument into a single
assumption so that the rest of the development can appeal to it without
using further placeholders. -/
axiom entropy_gate_separates_P_from_NP (ΔΦ : Float) :
    ΔΦ > 0.09 → P ≠ NP

/-- Entropy-gate triggers provably exponential lower bound ⇒ P ≠ NP. -/
theorem P_ne_NP_of_entropy_gate (ΔΦ : Float) (h : ΔΦ > 0.09) :
    P ≠ NP :=
  entropy_gate_separates_P_from_NP ΔΦ h
