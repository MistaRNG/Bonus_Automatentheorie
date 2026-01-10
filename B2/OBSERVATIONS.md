# Beobachtungen zur Korrektheit

## Quellcode-Analyse (kurz)

- **Potenzmengenkonstruktion on-the-fly**: Der Algorithmus konstruiert den DFA für das Komplement nicht vollständig, sondern nur die erreichbaren Zustände.
- **$\varepsilon$-Hüllen-Berechnung**: Für jeden Zustand wird die $\varepsilon$-Hülle berechnet, um $\varepsilon$-Transitionen korrekt zu behandeln.
- **Initiale Prüfung**: Wenn die $\varepsilon$-Hülle der Startzustände einen Endzustand enthält, wird $\varepsilon$ akzeptiert. In diesem Fall sucht der Algorithmus nach einem nicht-leeren Wort im Komplement.
- **BFS über Zustandsmengen**: Die BFS läuft über Mengen von Zuständen (Potenzmengenzustände) und folgt Übergängen über Symbole aus $\Sigma$.
- **Komplement-Endzustände**: Ein Potenzmengenzustand ist ein Endzustand im Komplement, wenn er **keinen** Endzustand des ursprünglichen Automaten enthält.
- **Pfadrekonstruktion**: Bei Erreichen eines Komplement-Endzustands wird das Wort durch Rückverfolgung der gespeicherten Vorgänger rekonstruiert.
- **Rückgabe**: Wird kein Komplement-Endzustand gefunden, ist $L(A)^c = \emptyset$ und es wird $\bot$ zurückgegeben.

## Tests (klein bis groß)

### `test_inputs/t1_initial_is_final.json` → Ausgabe: `⊥`
- **Automat**: Ein einziger Zustand `q0`, der sowohl Start- als auch Endzustand ist. Kein Alphabet, keine Transitionen.
- **$L(A)$**: $\{\varepsilon\}$ (nur das leere Wort wird akzeptiert)
- **$L(A)^c$**: Alle Wörter außer $\varepsilon$, aber da $\Sigma = \emptyset$, gibt es keine anderen Wörter → $L(A)^c = \emptyset$
- **Ergebnis**: $\bot$ 

### `test_inputs/t2_unreachable_final.json` → Ausgabe: `ε`
- **Automat**: Zwei Zustände `q0` (Start) und `q1` (Final), aber keine Transitionen.
- **$L(A)$**: $\emptyset$ (kein Endzustand erreichbar)
- **$L(A)^c$**: $\Sigma^* = \{ε, a, aa, aaa, \ldots\}$ (alle Wörter)
- **Ergebnis**: $\varepsilon$

### `test_inputs/t3_simple_word.json` → Ausgabe: `ε`
- **Automat**: Linearer Automat `q0 --a--> q1 --b--> q2` (nur `q2` ist final)
- **$L(A)$**: $\{ab\}$ (nur das Wort `ab` wird akzeptiert)
- **$L(A)^c$**: $\Sigma^* \setminus \{ab\} = \{ε, a, b, aa, ba, bb, aaa, \ldots\}$
- **Ergebnis**: $\varepsilon$

### `test_inputs/t4_epsilon_path.json` → Ausgabe: `a`
- **Automat**: `q0` (Start) mit $\varepsilon$-Transition zu `q1` (Final)
- **$L(A)$**: $\{\varepsilon\}$ (nur das leere Wort wird akzeptiert, da $\varepsilon$-Hülle von `q0` den Endzustand `q1` enthält)
- **$L(A)^c$**: $\Sigma^* \setminus \{\varepsilon\} = \{a, aa, aaa, \ldots\}$ (alle nicht-leeren Wörter)
- **Ergebnis**: `a` 

### `test_inputs/t5_nfa_branch.json` → Ausgabe: `ε`
- **Automat**: NFA mit Verzweigungen (mehrere Transitionen möglich)
- **$L(A)$**: Enthält mindestens ein nicht-leeres Wort
- **$L(A)^c$**: Enthält $\varepsilon$, da der Startzustand kein Endzustand ist
- **Ergebnis**: $\varepsilon$ 

### `test_inputs/t6_adj_dict.json` → Ausgabe: `ε`
- **Automat**: Verwendet Adjazenz-Dictionary-Format für Transitionen
- **$L(A)$**: Enthält mindestens ein nicht-leeres Wort (z.B. `b`)
- **$L(A)^c$**: Enthält $\varepsilon$
- **Ergebnis**: $\varepsilon$ 

### `test_inputs/t7_large.json` → Ausgabe: `ε`
- **Automat**: Größeres Beispiel mit mehreren Zuständen, Start- und Endzuständen
- **$L(A)$**: Komplexere Sprache mit mehreren akzeptierten Wörtern
- **$L(A)^c$**: Enthält $\varepsilon$, da nicht alle Startzustände gleichzeitig Endzustände sind
- **Ergebnis**: $\varepsilon$

### `test_inputs/t8_no_path.json` → Ausgabe: `a`
- **Automat**: Ein Zustand `q0`, der sowohl Start- als auch Endzustand ist. Alphabet $\{a, b\}$, aber keine Transitionen.
- **$L(A)$**: $\{\varepsilon\}$ (nur das leere Wort wird akzeptiert)
- **$L(A)^c$**: $\Sigma^* \setminus \{\varepsilon\} = \{a, b, aa, ab, ba, bb, \ldots\}$ (alle nicht-leeren Wörter)
- **Ergebnis**: `a`