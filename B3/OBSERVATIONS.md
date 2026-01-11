# Beobachtungen zur Korrektheit
Der Algorithmus baut den Produktautomaten von \(A_1\) und \(A_2\) nicht explizit, sondern erzeugt Produktzustände \((p,q)\) nur dann, wenn sie durch BFS erreichbar sind.

**\(\varepsilon\)-Hüllen-Berechnung:**  
Für beide Automaten wird zuerst die \(\varepsilon\)-Hülle der Startzustände berechnet; daraus entsteht die initiale Menge  
\(\varepsilon\text{-closure}(I_1)\times \varepsilon\text{-closure}(I_2)\).  
Zusätzlich werden während der BFS \(\varepsilon\)-Schritte in jedem Automaten separat als Produktkanten berücksichtigt.

**Initiale Prüfung:**  
Wenn bereits ein initiales Paar \((p,q)\) mit \(p\in F_1\) und \(q\in F_2\) existiert, ist \(\varepsilon\in L(A_1)\cap L(A_2)\) und das Programm gibt \(\varepsilon\) aus.

**BFS über Produktzustände:**  
Die BFS läuft über Paare \((p,q)\). Es gibt drei Arten von Nachfolgern:

- \(\varepsilon\)-Schritte in \(A_1\)
- \(\varepsilon\)-Schritte in \(A_2\)
- synchronisierte Symbolschritte \(a\in\Sigma\), die in beiden Automaten gleichzeitig möglich sind

**Schnitt-Endzustände:**  
Ein Produktzustand ist akzeptierend (Schnitt nicht leer), genau dann wenn beide Komponenten akzeptierend sind:  
\((p,q)\in F_1\times F_2\).

**Pfadrekonstruktion:**  
Zu jedem neu entdeckten Produktzustand wird ein Vorgänger samt konsumiertem Symbol gespeichert. Beim ersten akzeptierenden Produktzustand wird durch Rückverfolgung das Beispielwort rekonstruiert; \(\varepsilon\)-Kanten (Symbol = `None`) tragen kein Zeichen zum Wort bei.

**Rückgabe:**  
Wird kein akzeptierender Produktzustand erreicht, dann ist  
\(L(A_1)\cap L(A_2)=\emptyset\) und es wird \(\bot\) ausgegeben.

## Tests (klein bis gross)

- `test_inputs/b3_b4/t9_intersection_aa.json` -> Ausgabe: `aa`
- `test_inputs/b3_b4/t10_intersection_empty.json` -> Ausgabe: `⊥`
- `test_inputs/b3_b4/t11_intersection_epsilon.json` -> Ausgabe: `ε`
- `test_inputs/b3_b4/t12_intersection_is_epsilon.json` -> Ausgabe: `ε`
- `test_inputs/b3_b4/t13_inclusion_subset.json` -> Ausgabe: `ab`
- `test_inputs/b3_b4/t14_inclusion_counterexample.json` -> Ausgabe: `⊥`
- `test_inputs/b3_b4/t15_inclusion_epsilon.json` -> Ausgabe: `⊥`
