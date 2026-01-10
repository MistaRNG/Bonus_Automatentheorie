# Beobachtungen zur Korrektheit

## Quellcode-Analyse (kurz)

- A2 wird per Potenzmengenkonstruktion mit ε-Huellen determinisiert; Alphabet ist die Vereinigung aus beiden Automaten und allen Transitionen.
- Ein DFA-Zustand ist im Komplement akzeptierend, wenn er keinen Original-Endzustand von A2 enthaelt.
- BFS ueber Produkt (q1, S2) mit ε-Expansion nur in A1; Symbolschritte uebernehmen die DFA-Transition in A2.
- Akzeptierend, sobald q1 final ist und S2 komplement-final; `pred` rekonstruiert das Wort, ε wird uebersprungen.
- Wenn kein akzeptierender Produktzustand erreichbar ist, gilt L(A1) ⊆ L(A2) und es wird ⊥ ausgegeben.

## Tests (klein bis gross)

- `test_inputs/b3b4_intersection_aa.json` -> Ausgabe: `a`. Gegenbeispiel zur Inklusion gefunden.
- `test_inputs/b3b4_intersection_empty.json` -> Ausgabe: `a`. Gegenbeispiel zur Inklusion gefunden.
- `test_inputs/b3b4_intersection_epsilon.json` -> Ausgabe: `⊥`. Inklusion haelt.
- `test_inputs/b3b4_intersection_is_epsilon.json` -> Ausgabe: `⊥`. Inklusion haelt.
- `test_inputs/b3b4_inclusion_subset.json` -> Ausgabe: `⊥`. Inklusion haelt.
- `test_inputs/b3b4_inclusion_counterexample.json` -> Ausgabe: `a`. Gegenbeispiel zur Inklusion gefunden.
- `test_inputs/b3b4_inclusion_epsilon.json` -> Ausgabe: `ε`. Gegenbeispiel ε gefunden.
