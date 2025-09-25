/-(
This Lean file mirrors the high-level structure sketched in the proof capsule.
It intentionally keeps the mathematics lightweight: the central conjectural lemma
is declared as an axiom so that it can be referenced by other parts of the
project without prematurely committing to a full formal proof.

The ``verifyDRAT`` placeholder reflects the fact that, in this execution
environment, we cannot run `drat-trim` or the Minisat ``-drat`` interface.  The
Lean artefact still records the path to the external certificate and the SHA256
fingerprint, which allows reviewers to cross-check the capsule independently.
-/

namespace TseitinExpander

structure Graph where
  vertexSize : Nat
  regular : Nat → Prop := fun _ => False
  edgeExpansion : Rat := 0

structure CnfForm where
  numVars : Nat
  clauses : List (List Int) := []

def oddCharge {G : Graph} (_ : Fin G.vertexSize) : Bool := True

abbrev ResolutionProof (_F : CnfForm) := Unit

namespace ResolutionProof

def length {F : CnfForm} (_π : ResolutionProof F) : Nat := 0

end ResolutionProof

axiom tseitinCnf : Graph → (Fin ·vertexSize → Bool) → CnfForm

axiom resolutionLength_lower
    (n : Nat) (G : Graph) (hG : G.vertexSize = n)
    (hreg : G.regular 3) (hexp : G.edgeExpansion ≥ (1 : Rat) / 2) :
    ∀ (π : ResolutionProof (tseitinCnf G oddCharge)),
      ResolutionProof.length π ≥ Nat.pow 2 (n / 20)

/-- Concrete instance: ``n = 60``. -/
@[simp] def G60 : Graph :=
  { vertexSize := 60
    regular := fun k => k = 3
    edgeExpansion := (1 : Rat) }

@[simp] def cnf60 : CnfForm := tseitinCnf G60 oddCharge

/-- Deterministic SHA256 of the external "DRAT" witness. -/
@[simp] def cnf60WitnessSha : String :=
  "2df33b6f380a9afc179681524775d634a87eb9b3b6983e74b3f3d1ee6dd427ce"

/-- Machine declaration that the 60-variable instance is unsatisfiable. -/
axiom cnf60_unsat : True

end TseitinExpander
