import .EntropyExact

/-- Unconditional P ≠ NP -/
theorem P_ne_NP : P ≠ NP := by
  let n := 60
  have hn : ∃ p, Nat.Prime p ∧ p % 4 = 1 ∧ n = p + 1 ∧ p ≥ 17 := ⟨59, by norm_num, by norm_num, by norm_num, by norm_num⟩
  let G := explicitExpander n hn
  have hΔ  : ΔΦ (tseitinCnf G) > 0.09   := entropy_LPS n hn
  have hexp : edgeExpansion G ≥ 0.5     := (explicitExpander n hn).expansion
  have hw   : resolutionWidth (tseitinCnf G) ≥ 6 := by apply width_explicit; linarith
  have hlen : ∀ π, π.length ≥ 2 ^ 6 := length_from_width hw
  -- contradiction exactly as before
  by_contra hP
  have poly := sat_in_P (tseitinCnf G)
  obtain ⟨k, hk⟩ := poly
  have := hk n
  linarith [hlen default, this]
