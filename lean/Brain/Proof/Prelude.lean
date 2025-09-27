import Std
open Std

namespace Brain.Proof

instance instDecidableEqList (α) [DecidableEq α] : DecidableEq (List α) := inferInstance

-- Count with predicate (returns Nat)
def List.count? (xs : List α) (p : α → Bool) : Nat :=
  xs.foldl (fun acc x => if p x then acc + 1 else acc) 0

end Brain.Proof
