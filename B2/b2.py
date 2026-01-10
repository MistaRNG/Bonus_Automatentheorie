#!/usr/bin/env python3
import argparse
import json
import sys
from collections import deque
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, Set, FrozenSet

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

def find_witness_for_complement(
    states: Iterable[Any],
    alphabet: Iterable[Any],
    initials: Iterable[Any],
    finals: Iterable[Any],
    delta: Any,
) -> Optional[str]:
    Q = set(states)
    Sigma = set(_normalize_symbol(s) for s in alphabet if _normalize_symbol(s) is not None)
    I = set(initials)
    F = set(finals)
    transitions = _parse_transitions(delta)

    # Adjacency list for the original automaton
    adj: Dict[Any, List[Tuple[Optional[str], Any]]] = {}
    for p, a, q in transitions:
        adj.setdefault(p, []).append((a, q))

    # Compute ε-closure of initial state
    initial_state = frozenset(I)
    epsilon_closure = set(initial_state)
    queue = deque(initial_state)
    while queue:
        q = queue.popleft()
        for sym, r in adj.get(q, []):
            if sym is None:  # ε-transition
                if r not in epsilon_closure:
                    epsilon_closure.add(r)
                    queue.append(r)
    epsilon_closure = frozenset(epsilon_closure)

    # Check if ε is accepted (i.e., if ε-closure contains a final state)
    if any(q in F for q in epsilon_closure):
        # ε is accepted by A, so it is NOT in L(A)^c.
        # We need to find a non-empty word in L(A)^c.
        pass
    else:
        # ε is NOT accepted by A, so it is in L(A)^c.
        return ""

    # BFS to find a non-empty word in L(A)^c
    visited: Set[FrozenSet[Any]] = set()
    queue = deque()
    queue.append(epsilon_closure)
    visited.add(epsilon_closure)
    pred: Dict[FrozenSet[Any], Tuple[FrozenSet[Any], Optional[str]]] = {}

    while queue:
        current = queue.popleft()
        for sym in Sigma:
            next_state = set()
            for q in current:
                for transition_sym, r in adj.get(q, []):
                    if transition_sym == sym:
                        next_state.add(r)
            # Compute ε-closure of next_state
            next_state_closure = set(next_state)
            sub_queue = deque(next_state)
            while sub_queue:
                q = sub_queue.popleft()
                for sub_sym, r in adj.get(q, []):
                    if sub_sym is None:  # ε-transition
                        if r not in next_state_closure:
                            next_state_closure.add(r)
                            sub_queue.append(r)
            next_state_closure = frozenset(next_state_closure)
            if next_state_closure not in visited:
                visited.add(next_state_closure)
                pred[next_state_closure] = (current, sym)
                if not any(q in F for q in next_state_closure):
                    # This is a final state in the complement automaton
                    symbols: List[str] = []
                    cur = next_state_closure
                    while cur in pred:
                        prev, s = pred[cur]
                        if s is not None:
                            symbols.append(s)
                        cur = prev
                    symbols.reverse()
                    return "".join(symbols)
                queue.append(next_state_closure)
    return None


def _read_json_input(path: Optional[str]) -> Dict[str, Any]:
    if path:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return json.load(sys.stdin)

def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find a witness for the complement of an NFA (on the fly)."
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
        witness = find_witness_for_complement(
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
