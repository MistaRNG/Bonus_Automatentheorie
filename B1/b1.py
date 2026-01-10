#!/usr/bin/env python3
import argparse
import sys
from collections import deque
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from shared.automaton_common import (
    format_witness,
    parse_transitions,
    read_json_input,
)

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
    transitions = parse_transitions(delta)

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
    data = _demo_automaton() if args.demo else read_json_input(args.file)

    try:
        witness = find_witness(
            data["Q"], data.get("Sigma", []), data["I"], data["F"], data["Delta"]
        )
    except (KeyError, ValueError) as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2

    print(format_witness(witness))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
