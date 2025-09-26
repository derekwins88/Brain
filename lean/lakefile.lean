import Lake
open Lake DSL

package «brain» where
  -- Uncomment later to fail on sorry:
  -- moreServerArgs := #["--no-sorry"]
  -- Uncomment later to make warnings fail:
  -- buildArgs := #["-Werror"]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.23.0"
