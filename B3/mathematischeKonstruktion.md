Algorithmus: Alg_intersection_witness(A1, A2)

Ziel:
Gegeben zwei endliche Automaten A1 und A2 (ggf. mit ε-Übergängen),
liefere ein Beispielwort w ∈ L(A1) ∩ L(A2), falls der Schnitt nicht leer ist,
ansonsten gib ⊥ zurück.

Eingabe:
  A1 = (Q1, Σ, Δ1, I1, F1)
  A2 = (Q2, Σ, Δ2, I2, F2)
wobei Δi ⊆ Qi × (Σ ∪ {ε}) × Qi (ε optional).

Ausgabe:
  - ein Wort w, das von beiden Automaten akzeptiert wird (w ∈ L(A1) ∩ L(A2)),
  - oder ⊥, falls L(A1) ∩ L(A2) = ∅.

Idee:
Führe eine Multi-Source-BFS auf dem Produktzustandsraum Q1 × Q2 aus.
Speichere Vorgänger, um beim Erreichen eines akzeptierenden Produktzustands
ein Wort rekonstruieren zu können.

Definitionen:
- Produkt-Startmenge: I_prod := I1 × I2
- Produkt-Endzustände: F_prod := F1 × F2
- Produkt-Übergänge:
    Ein Produkt-Übergang ((p1, p2), x, (q1, q2)) existiert genau dann, wenn:
      (p1, x, q1) ∈ Δ1  UND  (p2, x, q2) ∈ Δ2
    wobei x ∈ Σ ∪ {ε}.

Algorithmus (BFS + Vorgänger-Rekonstruktion):

1) Initialisiere Produkt-Startmenge:
      I_prod := I1 × I2

2) Falls ein Startpaar bereits akzeptierend ist:
      Falls es (i1, i2) ∈ I_prod gibt mit i1 ∈ F1 und i2 ∈ F2:
           gib ε zurück

3) Initialisiere Multi-Source-BFS:
      W := Warteschlange mit allen Paaren aus I_prod
      V := Menge der besuchten Produktzustände, initial V := I_prod
      pred := leere Abbildung
        pred[(q1,q2)] = ((p1,p2), x) speichert Vorgänger-Paar und Symbol x
        pred ist für alle Startpaare aus I_prod undefiniert

4) Solange W nicht leer ist:
      (p1, p2) := entnimm vorn aus W

      Für jeden Produkt-Übergang ((p1,p2), x, (q1,q2)):
          // d.h.: (p1, x, q1) in Δ1 und (p2, x, q2) in Δ2
          Falls (q1,q2) ∉ V:
              füge (q1,q2) zu V hinzu
              pred[(q1,q2)] := ((p1,p2), x)

              Falls q1 ∈ F1 UND q2 ∈ F2:
                  // rekonstruiere ein Beispielwort
                  symbols := leere Liste
                  cur := (q1,q2)
                  Solange cur in pred:
                      (prev, sym) := pred[cur]
                      Falls sym ≠ ε:
                          füge sym zu symbols hinzu
                      cur := prev
                  drehe symbols um
                  w := konkatenation aller Symbole in symbols
                  gib w zurück   (w kann ε sein, wenn nur ε-Schritte vorkamen)

              füge (q1,q2) hinten an W an

5) Falls BFS endet, ohne einen akzeptierenden Produktzustand zu erreichen:
      gib ⊥ zurück
