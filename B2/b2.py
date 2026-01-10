#!/usr/bin/env python3
import argparse
import sys
from collections import deque
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, Set, FrozenSet

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from shared.automaton_common import (
    build_adj,
    epsilon_closure,
    format_witness,
    normalize_symbol,
    parse_transitions,
    read_json_input,
)

def find_witness_for_complement(
    states: Iterable[Any],
    alphabet: Iterable[Any],
    initials: Iterable[Any],
    finals: Iterable[Any],
    delta: Any,
) -> Optional[str]:
    Q = set(states)
    Sigma = set(normalize_symbol(s) for s in alphabet if normalize_symbol(s) is not None)
    I = set(initials)
    F = set(finals)
    transitions = parse_transitions(delta)
    adj = build_adj(transitions)

    initial_closure = epsilon_closure(I, adj)

    # Check if ε is accepted (i.e., if ε-closure contains a final state)
    if any(q in F for q in initial_closure):
        # ε is accepted by A, so it is NOT in L(A)^c.
        # We need to find a non-empty word in L(A)^c.
        pass
    else:
        # ε is NOT accepted by A, so it is in L(A)^c.
        return ""

    # BFS to find a non-empty word in L(A)^c
    visited: Set[FrozenSet[Any]] = set()
    queue = deque()
    queue.append(initial_closure)
    visited.add(initial_closure)
    pred: Dict[FrozenSet[Any], Tuple[FrozenSet[Any], Optional[str]]] = {}

    while queue:
        current = queue.popleft()
        for sym in Sigma:
            next_state = set()
            for q in current:
                for transition_sym, r in adj.get(q, []):
                    if transition_sym == sym:
                        next_state.add(r)
            next_state_closure = epsilon_closure(next_state, adj)
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
    data = _demo_automaton() if args.demo else read_json_input(args.file)

    try:
        witness = find_witness_for_complement(
            data["Q"], data.get("Sigma", []), data["I"], data["F"], data["Delta"]
        )
    except (KeyError, ValueError) as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2

    print(format_witness(witness))
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
