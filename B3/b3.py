#!/usr/bin/env python3
from __future__ import annotations

from collections import deque
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

EPSILON_SYMBOL = "\u03b5"  # 'ε'


def _normalize_symbol(sym: Any) -> Optional[str]:
    """Map epsilon-like encodings to None; keep other symbols as stripped strings."""
    if sym is None:
        return None
    if isinstance(sym, str):
        s = sym.strip()
        if s == "" or s.lower() in {"eps", "epsilon"} or s == EPSILON_SYMBOL:
            return None
        return s
    return str(sym)


def _parse_transitions(delta: Any) -> List[Tuple[Any, Optional[str], Any]]:
    """
    Accept either:
      - list/tuple of [p, a, q] or {"from": p, "symbol": a, "to": q}
      - adjacency dict {p: {symbol: [q1, q2]}} (targets may be single or list-like)
    Returns list of (p, normalized_symbol_or_None, q).
    """
    transitions: List[Tuple[Any, Optional[str], Any]] = []

    if isinstance(delta, dict):
        for p, sym_map in delta.items():
            if not isinstance(sym_map, dict):
                raise ValueError("Delta dict values must be dicts of symbol -> targets.")
            for sym, targets in sym_map.items():
                a = _normalize_symbol(sym)
                if isinstance(targets, (list, tuple, set)):
                    for q in targets:
                        transitions.append((p, a, q))
                else:
                    transitions.append((p, a, targets))
        return transitions

    if not isinstance(delta, (list, tuple)):
        raise ValueError("Delta must be a list/tuple or adjacency dict.")

    for item in delta:
        if isinstance(item, (list, tuple)) and len(item) == 3:
            p, a, q = item
            transitions.append((p, _normalize_symbol(a), q))
        elif isinstance(item, dict):
            p = item.get("from")
            a = item.get("symbol")
            q = item.get("to")
            if p is None or q is None:
                raise ValueError("Transition dict must have 'from' and 'to'.")
            transitions.append((p, _normalize_symbol(a), q))
        else:
            raise ValueError("Each transition must be a 3-tuple/list or a dict.")
    return transitions


def _index_transitions(
    transitions: Sequence[Tuple[Any, Optional[str], Any]]
) -> Tuple[
    Dict[Any, List[Any]],  # eps adjacency: p -> [q,...]
    Dict[Any, Dict[str, List[Any]]],  # sym adjacency: p -> {a: [q,...]}
]:
    eps_adj: Dict[Any, List[Any]] = {}
    sym_adj: Dict[Any, Dict[str, List[Any]]] = {}

    for p, a, q in transitions:
        if a is None:
            eps_adj.setdefault(p, []).append(q)
        else:
            sym_adj.setdefault(p, {}).setdefault(a, []).append(q)
    return eps_adj, sym_adj


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
    t1 = _parse_transitions(A1["Delta"])
    t2 = _parse_transitions(A2["Delta"])
    eps1, sym1 = _index_transitions(t1)
    eps2, sym2 = _index_transitions(t2)

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


# -------------------- Demo --------------------
if __name__ == "__main__":
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

    w = intersection_witness(A1, A2)
    if w is None:
        print("⊥")
    elif w == "":
        print("ε")
    else:
        print(w)
