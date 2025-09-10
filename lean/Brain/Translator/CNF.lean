import Brain.Translator.Clause

namespace Brain.Translator

structure CNF where
  clauses : List Clause
deriving Repr, DecidableEq

def cnfToString (f : CNF) : String :=
  String.intercalate " ∧ " (f.clauses.map clauseToString)

end Brain.Translator
