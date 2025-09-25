"""Utilities for generating Tseitin CNF benchmarks on small expanders.

The construction here keeps the implementation lightweight and dependency-free.
It builds a 3-regular graph by taking a cycle on ``n`` vertices and adding the
perfect matching that pairs each vertex ``v`` with ``v + n/2``.  Any connected
3-regular graph with an odd number of charged vertices yields an unsatisfiable
Tseitin instance, so the instance returned by :func:`dump_dimacs` is a convenient
source of deterministic UNSAT benchmarks.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


@dataclass(frozen=True)
class RegularGraph:
    """A very small helper type for the explicit 3-regular graph we build."""

    num_vertices: int
    edges: Tuple[Tuple[int, int], ...]

    def neighbors(self, v: int) -> Sequence[int]:
        """Return the neighbours of ``v`` in ascending order."""

        if v < 0 or v >= self.num_vertices:
            raise ValueError(f"vertex index {v} out of bounds for graph of size {self.num_vertices}")
        neigh: List[int] = []
        for a, b in self.edges:
            if a == v:
                neigh.append(b)
            elif b == v:
                neigh.append(a)
        neigh.sort()
        return neigh


def _cycle_with_matching_edges(n: int) -> Tuple[Tuple[int, int], ...]:
    """Create the edge set for the explicit 3-regular construction.

    The recipe is:
    * add the cycle ``(v, v + 1 mod n)`` to provide two edges per vertex;
    * add the perfect matching ``(v, v + n/2 mod n)`` to supply the third edge.

    The resulting multigraph is simple provided ``n`` is a positive even integer.
    """

    if n % 2 != 0 or n <= 0:
        raise ValueError("the explicit expander requires a positive even number of vertices")

    edges = set()

    for v in range(n):
        edges.add(tuple(sorted((v, (v + 1) % n))))
        edges.add(tuple(sorted((v, (v + n // 2) % n))))

    return tuple(sorted(edges))


def expander_graph(n: int) -> RegularGraph:
    """Return a deterministic 3-regular expander-like graph on ``n`` vertices."""

    edges = _cycle_with_matching_edges(n)
    return RegularGraph(num_vertices=n, edges=edges)


def tseitin_cnf(graph: RegularGraph, charged_vertices: Iterable[int] | None = None) -> List[List[int]]:
    """Create the Tseitin CNF for ``graph`` with an odd charge assignment.

    Parameters
    ----------
    graph:
        The underlying 3-regular graph whose edges become CNF variables.
    charged_vertices:
        Optional iterable describing which vertices receive charge ``1``.  When
        ``None`` the function charges only vertex ``0`` which guarantees that the
        total charge is odd and hence the instance is unsatisfiable.
    """

    charge_set = {int(v) for v in charged_vertices} if charged_vertices is not None else {0}
    if len(charge_set) % 2 == 0:
        raise ValueError("Tseitin instance is satisfiable when the number of charged vertices is even")

    # Assign an integer variable to each undirected edge.
    edge_to_var: Dict[Tuple[int, int], int] = {}
    for idx, (u, v) in enumerate(graph.edges, start=1):
        edge_to_var[(u, v)] = idx

    incidence: Dict[int, List[int]] = {v: [] for v in range(graph.num_vertices)}
    for (u, v), var in edge_to_var.items():
        incidence[u].append(var)
        incidence[v].append(var)

    clauses: List[List[int]] = []
    for vertex, variables in incidence.items():
        parity_one = 1 if vertex in charge_set else 0
        degree = len(variables)
        if degree == 0:
            continue
        for mask in range(1 << degree):
            if mask.bit_count() % 2 == parity_one:
                continue  # assignment satisfies the parity constraint
            clause: List[int] = []
            for i, var in enumerate(variables):
                bit = (mask >> i) & 1
                clause.append(-var if bit else var)
            clauses.append(clause)
    return clauses


def dump_dimacs(n: int, out: Path, charged_vertices: Iterable[int] | None = None) -> None:
    """Serialise the ``n``-vertex Tseitin instance to ``out`` in DIMACS CNF."""

    graph = expander_graph(n)
    cnf = tseitin_cnf(graph, charged_vertices)
    num_vars = len(graph.edges)

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as handle:
        handle.write(f"c 3-regular Tseitin expander on {graph.num_vertices} vertices\n")
        handle.write(f"p cnf {num_vars} {len(cnf)}\n")
        for clause in cnf:
            handle.write(" ".join(str(lit) for lit in clause) + " 0\n")


__all__ = [
    "RegularGraph",
    "expander_graph",
    "tseitin_cnf",
    "dump_dimacs",
]
