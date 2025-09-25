import json
import shutil
import subprocess
from pathlib import Path

import pytest

from brain.benchmarks.drat_check import drat_proof_and_hash
from brain.benchmarks.tseitin_expander import dump_dimacs


@pytest.mark.skipif(shutil.which("python") is None, reason="python interpreter not available")
def test_tseitin_pipeline(tmp_path: Path) -> None:
    cnf = tmp_path / "tseitin60.cnf"
    dump_dimacs(60, cnf)
    unsat, sha = drat_proof_and_hash(cnf)
    assert unsat

    capsule = json.loads(Path("capsules/tseitin_n60_proof.json").read_text(encoding="utf-8"))
    assert capsule["Metadata"]["drat_sha256"] == sha

    lake = shutil.which("lake")
    if lake is None:
        pytest.skip("Lean's lake build tool is not installed")

    result = subprocess.run(
        [lake, "build", "TseitinExpander.cnf60_unsat"],
        cwd=Path("brain/formal"),
        check=False,
    )
    assert result.returncode == 0
