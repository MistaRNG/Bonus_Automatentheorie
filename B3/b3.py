#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from collections import deque
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from shared.automaton_common import (
    format_witness,
    index_transitions,
    parse_transitions,
    read_json_input,
)


def intersection_witness(
    A1: Dict[str, Any],
    A2: Dict[str, Any],
) -> Optional[str]:
    """
    Implements Alg_intersection_witness(A1, A2).

    Input automata dicts use keys: Q, Sigma, I, F, Delta (like in your earlier code).
    Epsilon transitions can be encoded as None, "", "eps", "epsilon", or "ε".

    Returns:
      - ""  for epsilon (empty word)
      - "ab..." for a witness in L(A1) ∩ L(A2)
      - None if intersection is empty (⊥)
    """
    I1: Set[Any] = set(A1["I"])
    F1: Set[Any] = set(A1["F"])
    I2: Set[Any] = set(A2["I"])
    F2: Set[Any] = set(A2["F"])

    # Product start set I := I1 × I2
    I_prod: Set[Tuple[Any, Any]] = {(i1, i2) for i1 in I1 for i2 in I2}

    # If a start pair is already accepting -> ε
    for i1, i2 in I_prod:
        if i1 in F1 and i2 in F2:
            return ""

    # Parse and index transitions
    t1 = parse_transitions(A1["Delta"])
    t2 = parse_transitions(A2["Delta"])
    eps1, sym1 = index_transitions(t1)
    eps2, sym2 = index_transitions(t2)

    # Multi-source BFS init
    queue: deque[Tuple[Any, Any]] = deque(I_prod)
    visited: Set[Tuple[Any, Any]] = set(I_prod)
    pred: Dict[Tuple[Any, Any], Tuple[Tuple[Any, Any], Optional[str]]] = {}
    # pred[(q1,q2)] = ((p1,p2), x) where x in Σ ∪ {ε}; we represent ε as None

    # Helper: reconstruct word from accepting product state
    def reconstruct(end_pair: Tuple[Any, Any]) -> str:
        symbols: List[str] = []
        cur = end_pair
        while cur in pred:
            prev, x = pred[cur]
            if x is not None:
                symbols.append(x)
            cur = prev
        symbols.reverse()
        return "".join(symbols)

    # BFS
    while queue:
        p1, p2 = queue.popleft()

        # 1) epsilon moves in A1 only: ((p1,p2), ε, (q1,p2))
        for q1 in eps1.get(p1, []):
            nxt = (q1, p2)
            if nxt not in visited:
                visited.add(nxt)
                pred[nxt] = ((p1, p2), None)
                if q1 in F1 and p2 in F2:
                    return reconstruct(nxt)
                queue.append(nxt)

        # 2) epsilon moves in A2 only: ((p1,p2), ε, (p1,q2))
        for q2 in eps2.get(p2, []):
            nxt = (p1, q2)
            if nxt not in visited:
                visited.add(nxt)
                pred[nxt] = ((p1, p2), None)
                if p1 in F1 and q2 in F2:
                    return reconstruct(nxt)
                queue.append(nxt)

        # 3) symbol-synchronous moves:
        # For each symbol a where both have outgoing transitions, combine targets.
        out1 = sym1.get(p1, {})
        out2 = sym2.get(p2, {})
        if out1 and out2:
            common_syms = out1.keys() & out2.keys()
            for a in common_syms:
                for q1 in out1[a]:
                    for q2 in out2[a]:
                        nxt = (q1, q2)
                        if nxt in visited:
                            continue
                        visited.add(nxt)
                        pred[nxt] = ((p1, p2), a)
                        if q1 in F1 and q2 in F2:
                            return reconstruct(nxt)
                        queue.append(nxt)

    # No accepting product state reachable => empty intersection
    return None


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Intersection emptiness with witness for two (epsilon-)NFAs."
    )
    parser.add_argument("--file1", help="JSON file for automaton A1.")
    parser.add_argument("--file2", help="JSON file for automaton A2.")
    parser.add_argument(
        "--pair",
        help="JSON file containing {\"A1\": ..., \"A2\": ...}.",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run a small demo pair instead of reading input.",
    )
    return parser.parse_args(argv)


def _demo_automata() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    A1 = {
        "Q": ["s0", "s1", "s2"],
        "Sigma": ["a", "b"],
        "I": ["s0"],
        "F": ["s2"],
        "Delta": [
            ["s0", "a", "s1"],
            ["s1", "b", "s2"],
        ],
    }
    A2 = {
        "Q": ["t0", "t1", "t2"],
        "Sigma": ["a", "b"],
        "I": ["t0"],
        "F": ["t2"],
        "Delta": [
            ["t0", "a", "t1"],
            ["t1", "b", "t2"],
        ],
    }
    return A1, A2


def _load_automata(args: argparse.Namespace) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    if args.demo:
        return _demo_automata()
    if args.pair:
        data = read_json_input(args.pair)
        return data["A1"], data["A2"]
    if args.file1 or args.file2:
        if not (args.file1 and args.file2):
            raise ValueError("Provide both --file1 and --file2.")
        return read_json_input(args.file1), read_json_input(args.file2)
    data = read_json_input(None)
    return data["A1"], data["A2"]


def main(argv: Sequence[str]) -> int:
    args = _parse_args(argv)
    try:
        A1, A2 = _load_automata(args)
        witness = intersection_witness(A1, A2)
    except (KeyError, ValueError) as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2
    print(format_witness(witness))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
