# Beobachtungen zur Korrektheit

## Quellcode-Analyse (kurz)

- BFS ab allen Startzustaenden, `visited` verhindert Mehrfachbesuch; damit werden genau die von `I` erreichbaren Zustaende besucht.
- Wenn `I ∩ F` nicht leer ist, wird sofort das leere Wort akzeptiert (epsilon).
- Bei Erreichen eines finalen Zustands wird der erste gefundene Pfad via `pred` rekonstruiert; Symbole `epsilon` werden beim Wortaufbau uebersprungen.
- Damit wird ein akzeptiertes Wort gefunden, falls ein finaler Zustand erreichbar ist; sonst Rueckgabe `bottom`.

## Tests (klein bis gross)

- `test_inputs/t1_initial_is_final.json` -> Ausgabe: `epsilon`
  - Startzustand ist final; leeres Wort wird akzeptiert.
- `test_inputs/t2_unreachable_final.json` -> Ausgabe: `bottom`
  - Kein finaler Zustand erreichbar; Sprache leer.
- `test_inputs/t3_simple_word.json` -> Ausgabe: `ab`
  - Einfacher Pfad mit zwei Symbolen.
- `test_inputs/t4_epsilon_path.json` -> Ausgabe: `epsilon`
  - Final nur ueber epsilon-Kante erreichbar.
- `test_inputs/t5_nfa_branch.json` -> Ausgabe: `ad`
  - NFA mit Verzweigung; BFS findet einen gueltigen Pfad.
- `test_inputs/t6_adj_dict.json` -> Ausgabe: `b`
  - Adjazenz-Dict-Format; `eps` wird als epsilon erkannt.
- `test_inputs/t7_large.json` -> Ausgabe: z.B. `babc` oder `aabc`
  - Groesseres Beispiel mit mehreren Start- und Endzustaenden; Ausgabe kann variieren, ist aber akzeptierend.
