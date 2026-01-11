# Beobachtungen zur Korrektheit

## Quellcode-Analyse (kurz)

- Produkt-BFS ueber Zustaende (q1, q2); Startmenge I1 × I2; `visited` verhindert Mehrfachbesuch.
- ε-Transitionen werden separat in A1 und in A2 expandiert (Symbol `None`), ohne das andere Produktglied zu aendern.
- Synchrone Symbolschritte nur fuer gemeinsame Symbole; Zielpaare werden kombiniert.
- Akzeptierend, sobald beide Komponenten final sind; `pred` rekonstruiert das Wort, ε wird uebersprungen.
- Wenn kein akzeptierender Produktzustand erreichbar ist, ist der Schnitt leer und es wird ⊥ ausgegeben.

## Tests (klein bis gross)

- `test_inputs/b3_b4/t9_intersection_aa.json` -> Ausgabe: `aa`. Schnitt enthaelt das Wort "aa".
- `test_inputs/b3_b4/t10_intersection_empty.json` -> Ausgabe: `⊥`. Schnitt ist leer.
- `test_inputs/b3_b4/t11_intersection_epsilon.json` -> Ausgabe: `ε`. Beide akzeptieren ε.
- `test_inputs/b3_b4/t12_intersection_is_epsilon.json` -> Ausgabe: `ε`. Schnitt enthaelt ε.
- `test_inputs/b3_b4/t13_inclusion_subset.json` -> Ausgabe: `ab`. Schnitt enthaelt "ab".
- `test_inputs/b3_b4/t14_inclusion_counterexample.json` -> Ausgabe: `⊥`. Schnitt ist leer.
- `test_inputs/b3_b4/t15_inclusion_epsilon.json` -> Ausgabe: `⊥`. Schnitt ist leer.
