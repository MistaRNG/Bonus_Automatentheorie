# Beobachtungen zur Korrektheit

## Quellcode-Analyse (kurz)

- BFS ab allen Startzustaenden; `visited` verhindert Mehrfachbesuch und beschraenkt auf erreichbare Zustaende.
- Wenn $I \cap F \neq \emptyset$, wird sofort $\varepsilon$ akzeptiert.
- $\varepsilon$-Transitionen werden wie Kanten behandelt; bei der Rekonstruktion werden Symbole `None` uebersprungen.
- Bei erstem finalen Zustand wird per `pred` ein Witness rekonstruiert (kuerzeste Anzahl an Kanten).
- Falls kein finaler Zustand erreichbar ist, Rueckgabe $\bot$.

## Tests (klein bis gross)

### `test_inputs/b1_b2/t1_initial_is_final.json`
- **Automat**: Ein Zustand, Start = Final, keine Transitionen.
- **Ergebnis**: $\varepsilon$.

### `test_inputs/b1_b2/t2_unreachable_final.json`
- **Automat**: Finaler Zustand ist nicht erreichbar.
- **Ergebnis**: $\bot$.

### `test_inputs/b1_b2/t3_simple_word.json`
- **Automat**: Linearer Pfad $q_0 \xrightarrow{a} q_1 \xrightarrow{b} q_2$.
- **Ergebnis**: `ab`.

### `test_inputs/b1_b2/t4_epsilon_path.json`
- **Automat**: Final ueber $\varepsilon$-Kante erreichbar.
- **Ergebnis**: $\varepsilon$.

### `test_inputs/b1_b2/t5_nfa_branch.json`
- **Automat**: NFA mit Verzweigung.
- **Ergebnis**: `ad`.

### `test_inputs/b1_b2/t6_adj_dict.json`
- **Automat**: Adjazenz-Dict-Format mit `eps`.
- **Ergebnis**: `b`.

### `test_inputs/b1_b2/t7_large.json`
- **Automat**: Groesseres Beispiel mit mehreren Start- und Endzustaenden.
- **Ergebnis**: z.B. `babc` (abhaengig von der Kantenreihenfolge).

### `test_inputs/b1_b2/t8_no_path.json`
- **Automat**: Ein Zustand, Start = Final, keine Transitionen.
- **Ergebnis**: $\varepsilon$.
