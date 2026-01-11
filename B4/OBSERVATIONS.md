# Beobachtungen zur Korrektheit

## Quellcode-Analyse (kurz)

- $A_2$ wird per Potenzmengenkonstruktion mit $\varepsilon$-Huellen determinisiert; das Alphabet ist die Vereinigung beider Alphabete und aller Transitionen.
- Ein DFA-Zustand $S_2$ ist im Komplement akzeptierend, wenn $S_2 \cap F_2 = \emptyset$ gilt.
- BFS ueber Produkt $(q_1, S_2)$ mit $\varepsilon$-Expansion nur in $A_1$; Symbolschritte verwenden die DFA-Transition in $A_2$.
- Akzeptierend, sobald $q_1 \in F_1$ und $S_2$ komplement-final ist; `pred` rekonstruiert das Wort, $\varepsilon$ wird uebersprungen.
- Wenn kein akzeptierender Produktzustand erreichbar ist, gilt $L(A_1) \subseteq L(A_2)$ und es wird $\bot$ ausgegeben.

## Tests (klein bis gross)

### `test_inputs/b3_b4/t9_intersection_aa.json`
- **Ergebnis**: `a` (A1 akzeptiert `a`, A2 verlangt zwei `a`).

### `test_inputs/b3_b4/t10_intersection_empty.json`
- **Ergebnis**: `a` (A1 akzeptiert `a`, A2 akzeptiert nur `b`).

### `test_inputs/b3_b4/t11_intersection_epsilon.json`
- **Ergebnis**: $\bot$ (A1 akzeptiert nur $\varepsilon$, A2 akzeptiert $\varepsilon$; Inklusion gilt).

### `test_inputs/b3_b4/t12_intersection_is_epsilon.json`
- **Ergebnis**: $\bot$ (beide akzeptieren nur $\varepsilon$; Inklusion gilt).

### `test_inputs/b3_b4/t13_inclusion_subset.json`
- **Ergebnis**: $\bot$ ($L(A_1)=\{ab\} \subseteq L(A_2)$).

### `test_inputs/b3_b4/t14_inclusion_counterexample.json`
- **Ergebnis**: `a` (A1 akzeptiert `a`, A2 akzeptiert nur `b`).

### `test_inputs/b3_b4/t15_inclusion_epsilon.json`
- **Ergebnis**: $\varepsilon$ (A1 akzeptiert $\varepsilon$, A2 akzeptiert nichts).
