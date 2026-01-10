Gegeben ist ein endlicher Automat A = (Q, Σ, Δ, I, F).

- Q: endliche Menge von Zustaenden
- Σ: Alphabet
- I ⊆ Q: Menge der Startzustaende
- F ⊆ Q: Menge der akzeptierenden (finalen) Zustaende
- Δ: Transitionsrelation. Sie kann sein
  (1) NFA ohne Epsilon: Δ ⊆ Q × Σ × Q
  (2) NFA mit Epsilon:  Δ ⊆ Q × (Σ ∪ {ε}) × Q
  Verwenden Sie bei Bedarf ε als Epsilon-Symbol.

Aufgabe (Leerheit mit Zeuge):
Eingabe: A
Ausgabe:
- Falls L(A) ≠ ∅, gib ein Beispielwort w ∈ L(A) aus
- Sonst gib ⊥ aus

Algorithmus (BFS + Vorgaenger-Rekonstruktion):

1) Falls I ∩ F ≠ ∅:
   gib ε zurueck (leeres Wort akzeptiert)

2) Initialisierung:
   queue := alle Zustaende in I (Multi-Source-BFS)
   visited := I
   pred := leere Abbildung
     pred[q] speichert (p, a) mit:
     q wurde zuerst vom Vorgaenger p ueber Label a erreicht
     wobei a ∈ Σ oder a = ε

3) Solange queue nicht leer:
   p := pop_front(queue)

   Fuer jede Transition (p, a, q) in Δ:
     Falls q nicht in visited:
       visited.add(q)
       pred[q] := (p, a)

       Falls q ∈ F:
         // rekonstruiere ein Zeugenwort
         w_symbols := leere Liste
         cur := q
         Solange cur in pred:
           (prev, sym) := pred[cur]
           Falls sym ≠ ε:
             sym an w_symbols anhaengen
           cur := prev
         w_symbols umdrehen
         w := alle Symbole in w_symbols konkatenieren
         gib w zurueck (w kann ε sein, wenn nur ε-Kanten benutzt wurden)

     queue hinten anfuegen

4) Wenn keine finalen Zustaende erreicht wurden:
   gib ⊥ zurueck

Korrektheitsintuition:
- visited ist genau die Menge der von I erreichbaren Zustaende.
- L(A) ≠ ∅ genau dann, wenn ein Zustand in F von I erreichbar ist.
- pred speichert einen erreichbaren Pfad, daher liefert die Rekonstruktion ein
  Wort, das diesen Pfad beschriftet.