import Lake
open Lake DSL

package «brain» where
  moreServerArgs := #[]
  -- add buildArgs if you like: buildArgs := #["-Dlinter.missingDocs=false"]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"
