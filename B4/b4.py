#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from collections import deque
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple, FrozenSet

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


def _collect_sigma(
    alphabets: Iterable[Any],
    transitions: Iterable[Tuple[Any, Optional[str], Any]],
) -> List[str]:
    sigma: List[str] = []
    seen: Set[str] = set()
    for sym in alphabets:
        norm = normalize_symbol(sym)
        if norm is None:
            continue
        if norm not in seen:
            seen.add(norm)
            sigma.append(norm)
    for _, sym, _ in transitions:
        if sym is None:
            continue
        if sym not in seen:
            seen.add(sym)
            sigma.append(sym)
    return sigma


def _determinize_with_epsilon(
    initials: Iterable[Any],
    finals: Iterable[Any],
    transitions: Sequence[Tuple[Any, Optional[str], Any]],
    sigma: Sequence[str],
) -> Tuple[
    FrozenSet[Any],
    Dict[FrozenSet[Any], Dict[str, FrozenSet[Any]]],
    Set[Any],
]:
    adj = build_adj(transitions)
    start = epsilon_closure(initials, adj)
    det_transitions: Dict[FrozenSet[Any], Dict[str, FrozenSet[Any]]] = {}

    queue: deque[FrozenSet[Any]] = deque([start])
    visited: Set[FrozenSet[Any]] = {start}

    while queue:
        current = queue.popleft()
        trans_map: Dict[str, FrozenSet[Any]] = {}
        for sym in sigma:
            move_set: Set[Any] = set()
            for q in current:
                for a, r in adj.get(q, []):
                    if a == sym:
                        move_set.add(r)
            next_state = epsilon_closure(move_set, adj)
            trans_map[sym] = next_state
            if next_state not in visited:
                visited.add(next_state)
                queue.append(next_state)
        det_transitions[current] = trans_map

    return start, det_transitions, set(finals)


def inclusion_witness(A1: Dict[str, Any], A2: Dict[str, Any]) -> Optional[str]:
    I1 = set(A1["I"])
    F1 = set(A1["F"])

    t1 = parse_transitions(A1["Delta"])
    t2 = parse_transitions(A2["Delta"])
    adj1 = build_adj(t1)

    sigma = _collect_sigma(
        list(A1.get("Sigma", [])) + list(A2.get("Sigma", [])),
        list(t1) + list(t2),
    )

    start2, det2, F2 = _determinize_with_epsilon(A2["I"], A2["F"], t2, sigma)

    def is_complement_final(state2: FrozenSet[Any]) -> bool:
        return not any(q in F2 for q in state2)

    def is_accepting(state1: Any, state2: FrozenSet[Any]) -> bool:
        return state1 in F1 and is_complement_final(state2)

    start_pairs: Set[Tuple[Any, FrozenSet[Any]]] = {(q1, start2) for q1 in I1}
    if any(is_accepting(q1, start2) for q1 in I1):
        return ""

    queue: deque[Tuple[Any, FrozenSet[Any]]] = deque(start_pairs)
    visited: Set[Tuple[Any, FrozenSet[Any]]] = set(start_pairs)
    pred: Dict[
        Tuple[Any, FrozenSet[Any]],
        Tuple[Tuple[Any, FrozenSet[Any]], Optional[str]],
    ] = {}

    def reconstruct(end_pair: Tuple[Any, FrozenSet[Any]]) -> str:
        symbols: List[str] = []
        cur = end_pair
        while cur in pred:
            prev, sym = pred[cur]
            if sym is not None:
                symbols.append(sym)
            cur = prev
        symbols.reverse()
        return "".join(symbols)

    while queue:
        p1, s2 = queue.popleft()

        for sym, q1 in adj1.get(p1, []):
            if sym is None:
                nxt = (q1, s2)
                if nxt not in visited:
                    visited.add(nxt)
                    pred[nxt] = ((p1, s2), None)
                    if is_accepting(q1, s2):
                        return reconstruct(nxt)
                    queue.append(nxt)

        for sym, q1 in adj1.get(p1, []):
            if sym is None:
                continue
            next_s2 = det2.get(s2, {}).get(sym)
            if next_s2 is None:
                continue
            nxt = (q1, next_s2)
            if nxt in visited:
                continue
            visited.add(nxt)
            pred[nxt] = ((p1, s2), sym)
            if is_accepting(q1, next_s2):
                return reconstruct(nxt)
            queue.append(nxt)

    return None


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inclusion check with counterexample for two (epsilon-)NFAs."
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Alias for --pair (single JSON containing A1 and A2).",
    )
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
        "Q": ["s0", "s1"],
        "Sigma": ["a"],
        "I": ["s0"],
        "F": ["s1"],
        "Delta": [
            ["s0", "a", "s1"],
        ],
    }
    A2 = {
        "Q": ["t0"],
        "Sigma": ["a"],
        "I": ["t0"],
        "F": [],
        "Delta": [],
    }
    return A1, A2


def _load_automata(args: argparse.Namespace) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    if args.demo:
        return _demo_automata()
    if args.file:
        data = read_json_input(args.file)
        return data["A1"], data["A2"]
    if args.pair:
        data = read_json_input(args.pair)
        return data["A1"], data["A2"]
    data = read_json_input(None)
    return data["A1"], data["A2"]


def main(argv: Sequence[str]) -> int:
    args = _parse_args(argv)
    try:
        A1, A2 = _load_automata(args)
        witness = inclusion_witness(A1, A2)
    except (KeyError, ValueError) as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2
    print(format_witness(witness))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
