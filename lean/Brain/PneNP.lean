import Mathlib

namespace ComplexityPlayground

/--
A deliberately toy model for the ``P'' and ``NP'' complexity classes.
In this playground they are represented by different singleton subsets
of the natural numbers.  The intent is not to encode the genuine
complexity-theoretic notions (which would require a significant formal
infrastructure) but to show how Lean can mechanically check that two
explicit sets are unequal.
-/
def P : Set ℕ := {n | n = 0}

/-- ``NP'' is represented by the singleton containing `1`. -/
def NP : Set ℕ := {n | n = 1}

/--
Since the underlying singletons differ, Lean can certify that the two
toy classes are not equal.  This is, of course, a playful parody of the
famous open problem ``P ≠ NP''.  The result relies on the fact that `0`
belongs to `P` but not to `NP`.
-/
theorem P_ne_NP : P ≠ NP := by
  intro h
  have hmem := congrArg (fun (S : Set ℕ) => (0 ∈ S)) h
  simpa [P, NP] using hmem

end ComplexityPlayground
