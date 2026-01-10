Gegeben sind zwei endliche Automaten A1 = (Q1, Σ, Δ1, I1, F1) und
A2 = (Q2, Σ, Δ2, I2, F2).

- Q1, Q2: endliche Mengen von Zustaenden
- Σ: gemeinsames Alphabet
- I1 ⊆ Q1, I2 ⊆ Q2: Mengen der Startzustaende
- F1 ⊆ Q1, F2 ⊆ Q2: Mengen der akzeptierenden (finalen) Zustaende
- Δ1, Δ2: Transitionsrelationen. Sie koennen sein:
  (1) NFA ohne Epsilon: Δi ⊆ Qi × Σ × Qi
  (2) NFA mit Epsilon:  Δi ⊆ Qi × (Σ ∪ {ε}) × Qi
  Verwenden Sie bei Bedarf ε als Epsilon-Symbol.

Aufgabe (Inklusion mit Gegenbeispiel):
Eingabe: A1, A2
Ausgabe:
- Falls L(A1) ⊄ L(A2), gib ein Beispielwort w ∈ L(A1) \ L(A2) aus
- Sonst gib ⊥ aus (beliebiges Symbol fuer "L(A1) ⊆ L(A2)")

Grundidee (wie in der Aufgabenstellung):
L(A1) ⊆ L(A2)  ⇔  L(A1) ∩ (L(A2))^c = ∅

Also:
- Falls L(A1) ∩ (L(A2))^c nicht leer ist, liefert ein Wort daraus ein
  Gegenbeispiel w ∈ L(A1) \ L(A2).
- Falls diese Schnittsprache leer ist, gilt die Inklusion.

Algorithmus (Kombination aus B2, B3, B1):

1) Konstruiere das Komplement von A2 (aus B2):
   Erzeuge einen Automaten A2c mit:
     L(A2c) = (L(A2))^c
   (Hinweis: Falls notwendig, zuerst A2 determinisieren und komplettieren,
    dann akzeptierende Zustaende flippen.)

2) Konstruiere den Schnittautomaten (aus B3):
   Erzeuge einen Automaten Aint = A1 ∩ A2c mit:
     L(Aint) = L(A1) ∩ L(A2c)
            = L(A1) ∩ (L(A2))^c
            = L(A1) \ L(A2)

3) Fuehre Leerheit-mit-Zeuge auf Aint aus (aus B1):
   w := Alg_empty_witness(Aint)

   - Falls w ≠ ⊥:
       gib w zurueck
       (Dann gilt automatisch: w ∈ L(Aint) = L(A1) \ L(A2).)
   - Sonst:
       gib ⊥ zurueck
       (Dann ist L(Aint) = ∅ und damit L(A1) ⊆ L(A2).)

Korrektheitsintuition:
- Durch Komplement und Schnitt gilt: L(Aint) = L(A1) \ L(A2).
- Ein Witness w aus L(Aint) ist genau ein Gegenbeispiel zur Inklusion.
- Wenn kein Witness existiert (Sprache leer), kann es kein Gegenbeispiel geben,
  also muss L(A1) ⊆ L(A2) gelten.
