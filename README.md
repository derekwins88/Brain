# Brain

![CI - Python](https://github.com/derekwins88/Brain/actions/workflows/ci-python.yml/badge.svg)
![CI - .NET](https://github.com/derekwins88/Brain/actions/workflows/ci-dotnet.yml/badge.svg)

## Reproducibility & Ethics

Every stabilized run emits a **capsule** with:

1. `provenance.hashes.cnf_sha256` and `provenance.hashes.entropy_sha256`,
2. `provenance.sat_provenance` (mode `external|minisat` or `unit-contradiction`),
3. ethics toggles (`AXIOM_007`, `MirrorOnlyProtocol`, `DriftWallContainment`) recorded in the artifact.

If it isn’t auditable, it didn’t happen.
