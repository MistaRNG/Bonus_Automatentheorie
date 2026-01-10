# Algorithmus zur Findung eines Wortes im Komplement

## Idee

1. Falls $I \cap F \neq \emptyset$:
      - Der Automat akzeptiert $\varepsilon$.
      - Suche nach einem nicht-leeren Wort in $L(A)^c$.

2. Initialisierung:
   - Warteschlange $W := I$ (Multi-Source-BFS).
   - Besuchte Menge $V := I$.
   - Vorgängerabbildung $\text{pred}: Q \to (Q \times (\Sigma \cup \{\varepsilon\}))$ undefiniert für alle $q \in I$.

3. Solange $W \neq \emptyset$:
   - a. Entnehme $p$ aus $W$.
   - b. Für jeden Übergang $(p, a, q) \in \Delta$:
     - i. Falls $q \notin V$:
       - $V := V \cup \{q\}$.
       - $\text{pred}(q) := (p, a)$.
       - Falls $q \notin F$:
         - $q$ ist ein Endzustand des komplementären Automaten.
         - Rekonstruiere das Wort $w$ aus den Vorgängern und gib es zurück.
       - Füge $q$ zu $W$ hinzu.

4. Falls kein Endzustand des komplementären Automaten gefunden wurde:
   - Gib $\bot$ zurück (da $L(A)^c = \emptyset$).

---

### Rekonstruktion des Wortes $w$

Falls ein Endzustand $q_f$ des komplementären Automaten gefunden wurde:

1. Setze $q := q_f$ und $w := \varepsilon$.
2. Solange $\text{pred}(q)$ definiert ist:
   - a. Sei $\text{pred}(q) = (p, a)$.
   - b. Falls $a \neq \varepsilon$, setze $w := a \cdot w$ (Symbol vorne anhängen).
   - c. Setze $q := p$.
3. Gib $w$ zurück.

---

### Korrektheit

#### BFS/Erreichbarkeit

Die BFS findet alle von $I$ aus erreichbaren Zustände.

- Wird ein Zustand $q \notin F$ erreicht, liefert der gespeicherte Vorgängerpfad ein Wort, das nicht akzeptiert wird.
- Wird kein solcher Zustand erreicht, existiert kein akzeptierender Pfad im komplementären Automaten $\Rightarrow L(A)^c = \emptyset$.

## Pseudocode 

```plaintext
function find_witness_for_complement(A = (Q, Σ, Δ, I, F)):
    if I ∩ F ≠ ∅:
        # ε wird akzeptiert, also suche nach einem nicht-leeren Wort in L(A)^c.
        pass

    W := I  # Warteschlange
    V := I  # Besuchte Zustände
    pred := {}  # Vorgängerabbildung

    while W ≠ ∅:
        p := W.dequeue()
        for (p, a, q) in Δ:
            if q ∉ V:
                V := V ∪ {q}
                pred[q] := (p, a)
                if q ∉ F:
                    # q ist ein Endzustand des komplementären Automaten.
                    w := reconstruct_word(q, pred)
                    return w
                W.enqueue(q)

    return ⊥  # L(A)^c = ∅

function reconstruct_word(q, pred):
    w := ε
    while q in pred:
        (p, a) := pred[q]
        if a ≠ ε:
            w := a · w
        q := p
    return w
```

