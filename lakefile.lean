import Lake
open Lake DSL

package «Brain» where
  -- default

lean_lib «Brain» where
  srcDir := "lean"
  -- default

@[default_target]
lean_exe «proof» where
  root := `Brain.Proof.KWitness
  srcDir := "lean"
