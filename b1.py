#!/usr/bin/env python3
import argparse
import json
import sys
from collections import deque
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

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


def find_witness(
    states: Iterable[Any],
    alphabet: Iterable[Any],
    initials: Iterable[Any],
    finals: Iterable[Any],
    delta: Any,
) -> Optional[str]:
    _ = list(states)
    _ = list(alphabet)
    I = set(initials)
    F = set(finals)
    transitions = _parse_transitions(delta)

    if I & F:
        return ""

    queue: deque[Any] = deque(I)
    visited = set(I)
    pred: Dict[Any, Tuple[Any, Optional[str]]] = {}

    adj: Dict[Any, List[Tuple[Optional[str], Any]]] = {}
    for p, a, q in transitions:
        adj.setdefault(p, []).append((a, q))

    while queue:
        p = queue.popleft()
        for a, q in adj.get(p, []):
            if q in visited:
                continue
            visited.add(q)
            pred[q] = (p, a)
            if q in F:
                symbols: List[str] = []
                cur = q
                while cur in pred:
                    prev, sym = pred[cur]
                    if sym is not None:
                        symbols.append(sym)
                    cur = prev
                symbols.reverse()
                return "".join(symbols)
            queue.append(q)
    return None


def _read_json_input(path: Optional[str]) -> Dict[str, Any]:
    if path:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return json.load(sys.stdin)


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Emptiness check with witness for a (epsilon-)NFA using BFS."
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Read automaton JSON from file; otherwise read from stdin.",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run a small demo automaton instead of reading input.",
    )
    return parser.parse_args(argv)


def _demo_automaton() -> Dict[str, Any]:
    return {
        "Q": ["q0", "q1", "q2"],
        "Sigma": ["a", "b"],
        "I": ["q0"],
        "F": ["q2"],
        "Delta": [
            ["q0", "a", "q1"],
            ["q1", "b", "q2"],
        ],
    }


def main(argv: Sequence[str]) -> int:
    args = _parse_args(argv)
    data = _demo_automaton() if args.demo else _read_json_input(args.file)

    try:
        witness = find_witness(
            data["Q"], data.get("Sigma", []), data["I"], data["F"], data["Delta"]
        )
    except (KeyError, ValueError) as exc:
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
