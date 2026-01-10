#!/usr/bin/env python3
import argparse
import json
import sys
from collections import deque
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, Set

EPSILON_SYMBOL = "\u03b5"  # Greek small epsilon


def _normalize_symbol(sym: Any) -> Optional[str]:
    if sym is None:
        return None
    if isinstance(sym, str):
        s = sym.strip()
        if s == "" or s.lower() in {"eps", "epsilon"} or s == EPSILON_SYMBOL:
            return None
        return s
    return str(sym)


def _parse_transitions(delta: Any) -> List[Tuple[Any, Optional[str], Any]]:
    transitions: List[Tuple[Any, Optional[str], Any]] = []
    if isinstance(delta, dict):
        # Allow adjacency dict: {state: {symbol: [q1, q2]}}
        for p, sym_map in delta.items():
            if not isinstance(sym_map, dict):
                raise ValueError("Delta dict values must be dicts of symbol -> targets.")
            for sym, targets in sym_map.items():
                sym_norm = _normalize_symbol(sym)
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


class NFA:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.Q = set(data["Q"])
        self.Sigma = set(data.get("Sigma", []))
        self.I = set(data["I"])
        self.F = set(data["F"])
        transitions = _parse_transitions(data["Delta"])

        self.eps: Dict[Any, List[Any]] = {}
        self.sym: Dict[Any, Dict[str, List[Any]]] = {}

        for p, a, q in transitions:
            if a is None:
                self.eps.setdefault(p, []).append(q)
            else:
                self.sym.setdefault(p, {}).setdefault(a, []).append(q)

    def epsilon_closure(self, starts: Iterable[Any]) -> Set[Any]:
        closure: Set[Any] = set(starts)
        dq: deque[Any] = deque(starts)
        while dq:
            p = dq.popleft()
            for q in self.eps.get(p, []):
                if q not in closure:
                    closure.add(q)
                    dq.append(q)
        return closure


Pair = Tuple[Any, Any]


def find_witness_intersection(a1: NFA, a2: NFA) -> Optional[str]:
    # Initial pairs = eps-closure(I1) x eps-closure(I2)
    I1c = a1.epsilon_closure(a1.I)
    I2c = a2.epsilon_closure(a2.I)
    initial_pairs: Set[Pair] = {(p, q) for p in I1c for q in I2c}

    # If any initial pair is accepting -> epsilon witness
    for p, q in initial_pairs:
        if p in a1.F and q in a2.F:
            return ""

    queue: deque[Pair] = deque(initial_pairs)
    visited: Set[Pair] = set(initial_pairs)
    pred: Dict[Pair, Tuple[Pair, Optional[str]]] = {}

    def reconstruct(end: Pair) -> str:
        symbols: List[str] = []
        node = end
        while node in pred:
            prev, sym = pred[node]
            if sym is not None:
                symbols.append(sym)
            node = prev
        symbols.reverse()
        return "".join(symbols)

    def try_enqueue(cur: Pair, nxt: Pair, consumed: Optional[str]) -> Optional[str]:
        if nxt in visited:
            return None
        visited.add(nxt)
        pred[nxt] = (cur, consumed)

        p2, q2 = nxt
        if p2 in a1.F and q2 in a2.F:
            return reconstruct(nxt)

        queue.append(nxt)
        return None

    while queue:
        p, q = queue.popleft()
        cur = (p, q)

        # epsilon moves in A1
        for p2 in a1.eps.get(p, []):
            w = try_enqueue(cur, (p2, q), None)
            if w is not None:
                return w

        # epsilon moves in A2
        for q2 in a2.eps.get(q, []):
            w = try_enqueue(cur, (p, q2), None)
            if w is not None:
                return w

        # symbol moves on same symbol in both
        out1 = a1.sym.get(p, {})
        out2 = a2.sym.get(q, {})
        if not out1 or not out2:
            continue

        # iterate over intersection of keys
        if len(out1) <= len(out2):
            for sym, targets1 in out1.items():
                targets2 = out2.get(sym)
                if not targets2:
                    continue
                for p2 in targets1:
                    for q2 in targets2:
                        w = try_enqueue(cur, (p2, q2), sym)
                        if w is not None:
                            return w
        else:
            for sym, targets2 in out2.items():
                targets1 = out1.get(sym)
                if not targets1:
                    continue
                for p2 in targets1:
                    for q2 in targets2:
                        w = try_enqueue(cur, (p2, q2), sym)
                        if w is not None:
                            return w

    return None


def _read_json_file(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Intersection emptiness check with witness for (epsilon-)NFAs using product BFS."
    )
    parser.add_argument("--a1", required=True, help="Read automaton A1 JSON from file.")
    parser.add_argument("--a2", required=True, help="Read automaton A2 JSON from file.")
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> int:
    args = _parse_args(argv)

    try:
        data1 = _read_json_file(args.a1)
        data2 = _read_json_file(args.a2)

        A1 = NFA(data1)
        A2 = NFA(data2)

        witness = find_witness_intersection(A1, A2)
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2

    if witness is None:
        print("\u22a5")  # bottom symbol
    elif witness == "":
        print(EPSILON_SYMBOL)
    else:
        print(witness)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
