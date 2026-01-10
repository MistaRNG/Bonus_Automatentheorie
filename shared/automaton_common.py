#!/usr/bin/env python3
from __future__ import annotations

from collections import deque
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, FrozenSet

EPSILON_SYMBOL = "\u03b5"
BOTTOM_SYMBOL = "\u22a5"


def normalize_symbol(sym: Any) -> Optional[str]:
    if sym is None:
        return None
    if isinstance(sym, str):
        s = sym.strip()
        if s == "" or s.lower() in {"eps", "epsilon"} or s == EPSILON_SYMBOL:
            return None
        return s
    return str(sym)


def parse_transitions(delta: Any) -> List[Tuple[Any, Optional[str], Any]]:
    transitions: List[Tuple[Any, Optional[str], Any]] = []
    if isinstance(delta, dict):
        for p, sym_map in delta.items():
            if not isinstance(sym_map, dict):
                raise ValueError("Delta dict values must be dicts of symbol -> targets.")
            for sym, targets in sym_map.items():
                sym_norm = normalize_symbol(sym)
                if isinstance(targets, (list, tuple, set)):
                    for q in targets:
                        transitions.append((p, sym_norm, q))
                else:
                    transitions.append((p, sym_norm, targets))
        return transitions

    if not isinstance(delta, (list, tuple)):
        raise ValueError("Delta must be a list/tuple or adjacency dict.")

    for item in delta:
        if isinstance(item, (list, tuple)) and len(item) == 3:
            p, a, q = item
            transitions.append((p, normalize_symbol(a), q))
        elif isinstance(item, dict):
            p = item.get("from")
            a = item.get("symbol")
            q = item.get("to")
            if p is None or q is None:
                raise ValueError("Transition dict must have 'from' and 'to'.")
            transitions.append((p, normalize_symbol(a), q))
        else:
            raise ValueError("Each transition must be a 3-tuple/list or a dict.")
    return transitions


def build_adj(
    transitions: Sequence[Tuple[Any, Optional[str], Any]]
) -> Dict[Any, List[Tuple[Optional[str], Any]]]:
    adj: Dict[Any, List[Tuple[Optional[str], Any]]] = {}
    for p, a, q in transitions:
        adj.setdefault(p, []).append((a, q))
    return adj


def index_transitions(
    transitions: Sequence[Tuple[Any, Optional[str], Any]]
) -> Tuple[
    Dict[Any, List[Any]],
    Dict[Any, Dict[str, List[Any]]],
]:
    eps_adj: Dict[Any, List[Any]] = {}
    sym_adj: Dict[Any, Dict[str, List[Any]]] = {}

    for p, a, q in transitions:
        if a is None:
            eps_adj.setdefault(p, []).append(q)
        else:
            sym_adj.setdefault(p, {}).setdefault(a, []).append(q)
    return eps_adj, sym_adj


def epsilon_closure(
    start_states: Iterable[Any],
    adj: Dict[Any, List[Tuple[Optional[str], Any]]],
) -> FrozenSet[Any]:
    closure = set(start_states)
    queue = deque(start_states)
    while queue:
        q = queue.popleft()
        for sym, r in adj.get(q, []):
            if sym is None and r not in closure:
                closure.add(r)
                queue.append(r)
    return frozenset(closure)


def read_json_input(path: Optional[str]) -> Dict[str, Any]:
    import json
    import sys

    if path:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return json.load(sys.stdin)


def format_witness(witness: Optional[str]) -> str:
    if witness is None:
        return BOTTOM_SYMBOL
    if witness == "":
        return EPSILON_SYMBOL
    return witness
