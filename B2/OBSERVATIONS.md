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

### `t1_initial_is_final.json`
- **Automat**: Ein einziger Zustand $q0$, der sowohl Start- als auch Endzustand ist. Kein Alphabet, keine Transitionen.
- **$L(A)$**: $\{\varepsilon\}$ (nur das leere Wort wird akzeptiert)
- **$L(A)^c$**: Alle Wörter außer $\varepsilon$, aber da $\Sigma = \emptyset$, gibt es keine anderen Wörter → $L(A)^c = \emptyset$
- **Ergebnis**: $\bot$ 

### `t2_unreachable_final.json`
- **Automat**: Zwei Zustände $q0$ (Start) und $q1$ (Final), aber keine Transitionen.
- **$L(A)$**: $\emptyset$ (kein Endzustand erreichbar)
- **$L(A)^c$**: $\Sigma^* = \{ε, a, aa, aaa, \ldots\}$ (alle Wörter)
- **Ergebnis**: $\varepsilon$

### `t3_simple_word.json`
- **Automat**: Linearer Automat $q_0 \xrightarrow{a} q_1 \xrightarrow{b} q_2$ (nur $q_2$ ist final)
- **$L(A)$**: $\{ab\}$ (nur das Wort $ab$ wird akzeptiert)
- **$L(A)^c$**: $\Sigma^* \setminus \{ab\} = \{ε, a, b, aa, ba, bb, aaa, \ldots\}$
- **Ergebnis**: $\varepsilon$

### `t4_epsilon_path.json`
- **Automat**: $q0$ (Start) mit $\varepsilon$-Transition zu $q1$ (Final)
- **$L(A)$**: $\{\varepsilon\}$ (nur das leere Wort wird akzeptiert, da $\varepsilon$-Hülle von $q0$ den Endzustand $q1$ enthält)
- **$L(A)^c$**: $\Sigma^* \setminus \{\varepsilon\} = \{a, aa, aaa, \ldots\}$ (alle nicht-leeren Wörter)
- **Ergebnis**: $a$ 

### `t5_nfa_branch.json`
- **Automat**: NFA mit Verzweigungen (mehrere Transitionen möglich)
- **$L(A)$**: Enthält mindestens ein nicht-leeres Wort
- **$L(A)^c$**: Enthält $\varepsilon$, da der Startzustand kein Endzustand ist
- **Ergebnis**: $\varepsilon$ 

### `t6_adj_dict.json`
- **Automat**: Verwendet Adjazenz-Dictionary-Format für Transitionen
- **$L(A)$**: Enthält mindestens ein nicht-leeres Wort (z.B. $b$)
- **$L(A)^c$**: Enthält $\varepsilon$
- **Ergebnis**: $\varepsilon$ 

### `t7_large.json`
- **Automat**: Größeres Beispiel mit mehreren Zuständen, Start- und Endzuständen
- **$L(A)$**: Komplexere Sprache mit mehreren akzeptierten Wörtern
- **$L(A)^c$**: Enthält $\varepsilon$, da nicht alle Startzustände gleichzeitig Endzustände sind
- **Ergebnis**: $\varepsilon$

### `t8_no_path.json`
- **Automat**: Ein Zustand $q0$, der sowohl Start- als auch Endzustand ist. Alphabet $\{a, b\}$, aber keine Transitionen.
- **$L(A)$**: $\{\varepsilon\}$ (nur das leere Wort wird akzeptiert)
- **$L(A)^c$**: $\Sigma^* \setminus \{\varepsilon\} = \{a, b, aa, ab, ba, bb, \ldots\}$ (alle nicht-leeren Wörter)
- **Ergebnis**: $a$