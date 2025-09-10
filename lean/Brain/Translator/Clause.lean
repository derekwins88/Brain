namespace Brain.Translator

structure Literal where
  name    : String
  negated : Bool
deriving Repr, DecidableEq

def mkLiteral (s : String) (neg := false) : Literal :=
  { name := s, negated := neg }

structure Clause where
  lits : List Literal
deriving Repr, DecidableEq

def clauseToString (c : Clause) : String :=
  String.intercalate " ∨ "
    (c.lits.map (fun l => if l.negated then "¬" ++ l.name else l.name))

end Brain.Translator
