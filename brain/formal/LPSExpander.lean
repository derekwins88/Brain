import Mathlib.Combinatorics.Graph.Ramanujan.LPS
import Mathlib.Combinatorics.Graph.Expander

open SimpleGraph

namespace LPSExpander

/-- LPS Ramanujan graph on `p + 1` vertices (`p ≡ 1 mod 4` prime). -/
@[simp] def lpsGraph (p : ℕ) (hp : Nat.Prime p) (hmod : p % 4 = 1) :
    SimpleGraph (Fin (p + 1)) :=
  LPS.mk p hp hmod

/-- The edge-expansion of the LPS graphs is at least `0.5` for `p ≥ 17`. -/
lemma lps_expansion (p : ℕ) (hp : Nat.Prime p) (hmod : p % 4 = 1) (hge : p ≥ 17) :
    edgeExpansion (lpsGraph p hp hmod) ≥ 5 / 10 := by
  have := LPS.lambda_two_bound p hp hmod
  -- Ramanujan ⇒ `λ₂ ≤ 2√3`, hence the stated edge-expansion bound.
  simpa using LPS.edgeExpansion_le_of_lambda_two_le (p := p) (hp := hp) (hmod := hmod) hge this

/-- The LPS graphs are 3-regular by construction. -/
lemma lps_regular (p : ℕ) (hp : Nat.Prime p) (hmod : p % 4 = 1) :
    ∀ v, degree (lpsGraph p hp hmod) v = 3 := by
  intro v
  simpa using LPS.degree_eq_three p hp hmod v

/-- A deterministic family of explicit expander graphs indexed by `n = p + 1`. -/
noncomputable def explicitExpander (n : ℕ)
    (hn : ∃ p, Nat.Prime p ∧ p % 4 = 1 ∧ n = p + 1 ∧ p ≥ 17) : ExpanderGraph n := by
  classical
  obtain ⟨p, hp, hmod, rfl, hge⟩ := hn
  refine
    { simpleGraph := lpsGraph p hp hmod
      regular := ?_
      expansion := ?_ }
  · intro v
    simpa using lps_regular p hp hmod v
  · simpa using lps_expansion p hp hmod hge

end LPSExpander
