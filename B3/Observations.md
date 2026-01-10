Beobachtungen zur Korrektheit
Quellcode-Analyse (kurz)
**Produktautomat on-the-fly:**  
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

Tests
test_inputs/A1.json und A2.json -> Ausgabe: ab.
A1 akzeptiert genau ab, A2 akzeptiert Wörter die mit a beginnen; Schnitt wäre ab;
test_inputs/A1.json und A3.json -> Ausgabe: ab
A1 akzeptiert genau ab, A3 akzeptiert Wörter mit Suffix b; Schnitt wäre ab;
test_inputs/A1.json und A4.json -> Ausgabe: ⊥
A1 akzeptiert genau ab, A4 akzeptiert Wörter aus a; Schnitt ist leer;
test_inputs/A1.json und A5.json -> Ausgabe: ⊥
A1 akzeptiert genau ab, A5 akzeptiert nur ba; Schnitt ist leer;
test_inputs/A6.json und A7.json -> Ausgabe: ε
A6 akzeptiert ε und a, A7 akzeptiert ε über ε-Übergang; Schnitt ist ε;
