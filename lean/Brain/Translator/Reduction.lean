namespace Brain.Translator

/-- Very light placeholder notion of a reduction (A → B). -/
structure Reduction (A B : Type) where
  f : A → B

-- TODO: Extend with time bounds, composition, identity, etc.

end Brain.Translator
