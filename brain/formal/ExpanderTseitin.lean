import Mathlib.ComplexityTheory.CNF.Resolution
import Mathlib.Combinatorics.Graph.Expander
import DRAT.Verify

open DRAT Finset

namespace ExpanderTseitin

/-- 3-regular graph with edge-expansion ≥ 0.5 -/
structure ExpanderGraph (n : ℕ) where
  simpleGraph : SimpleGraph (Fin n)
  regular     : ∀ v, simpleGraph.degree v = 3
  expansion   : simpleGraph.edgeExpander ≥ 5 / 10

/-- Tseitin CNF with odd charge -/
def tseitinCnf {n} (G : ExpanderGraph n) : CnfForm :=
  let vars := (univ : Finset (Fin n)).val
  let oddCharge (v : Fin n) := true
  Tseitin.tseitinCnf G.simpleGraph oddCharge

/-- Resolution-width lower bound for expander Tseitin (Ben-Sasson–Wigderson) -/
lemma resolutionWidth_lower {n} (G : ExpanderGraph n) :
    resolutionWidth (tseitinCnf G) ≥ n / 10 := by
  apply Tseitin.width_lower_bound
  · exact G.regular
  · exact G.expansion

/-- Width → Size → Length lemma (classic) -/
lemma resolutionLength_lower {n} (G : ExpanderGraph n) :
    ∀ (π : ResolutionProof (tseitinCnf G)), π.length ≥ 2 ^ (resolutionWidth (tseitinCnf G) / 2) := by
  intro π
  apply Resolution.size_vs_width
  exact resolutionWidth_lower G

end ExpanderTseitin
