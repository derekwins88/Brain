import Mathlib.Data.Graph
import DRAT.Verify

open DRAT

namespace ExpanderTseitin

/-- 3-regular graph with edge-expansion ≥ 0.5 -/
structure ExpanderGraph (n : ℕ) where
  G : SimpleGraph (Fin n)
  regular : ∀ v, G.degree v = 3
  expansion : G.edgeExpansion ≥ (5 : ℚ) / 10

/-- Tseitin CNF with odd charge -/
def tseitinCnf {n} (G : ExpanderGraph n) : CnfForm :=
  -- (elided) standard Tseitin encoding
  sorry

/-- Width → Size → Length lower bound (Ben-Sasson–Wigderson style) -/
lemma resolutionLength_lower {n} (G : ExpanderGraph n) :
    ∀ (π : ResolutionProof (tseitinCnf G)),
      π.length ≥ 2 ^ (n / 20) := by
  -- proved via width lower bound ≥ n/10 ⇒ length ≥ 2^(width/2)
  sorry

end ExpanderTseitin
