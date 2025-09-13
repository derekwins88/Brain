from brain.unified_engine import UnifiedEngine


def test_np_wall_signal_triggers_hedge():
    engine = UnifiedEngine()
    cap = engine.run_engine(["⥁", "⚛"])
    assert cap.proof_claim == "P≠NP"
    assert cap.financial_forecast["action"] == "hedge"
    assert cap.ethical_audit["status"] == "Harmonic"


def test_contradiction_forks_paths():
    engine = UnifiedEngine()
    cap = engine.run_engine(["A", "NOT:A"])
    assert cap.proof_claim == "Contradiction"
    assert cap.fork_paths
