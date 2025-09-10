import Lake
open Lake DSL

package brain where
  buildArgs := #["-Werror"]  -- treat warnings as errors (incl. sorry); relax if needed

require mathlib from git
  "https://github.com/leanprover-community/mathlib4"
