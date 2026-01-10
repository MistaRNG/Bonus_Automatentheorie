# Bonus Automatentheorie

Ein Python-Programm zur Leerheitspruefung von (ε-)NFAs mit Ausgabe
eines konkreten akzeptierten Wortes, falls die Sprache nicht leer ist.

## Was ist das Leerheitsproblem?

Beim Leerheitsproblem fragt man: Ist die von einem Automaten akzeptierte Sprache
leer, also gilt L(A) = ∅? Falls nicht, moechte man oft ein Beispielwort w mit
w ∈ L(A). In dieser Aufgabe wird genau das entschieden und bei Nicht-Leerheit
ein Zeuge (Beispielwort) ausgegeben.

## Entscheidungen fuer die Abgabe

### Verwendete LLMs

#### Aufgabe B1: OpenAI Codex (GPT-5.2-Codex).
**Grund**: Zum Aufgabenzeitpunkt ist GPT-5.2-Codex das leistungsfaehigste Modell
fuer produktives Arbeiten in der IDE (Code-Vervollstaendigung, Refactoring,
schnelle Iteration von Implementierungsdetails, Debugging-Hinweise).
Dem Modell wurde ein zuvor selbsterarbeiteter, mathematisch exakter
Pseudocode (BFS-Erreichbarkeitspruefung mit Vorgaengerrekonstruktion zur
Witness-Erzeugung) uebergeben, und die Implementierung wurde daran
ausgerichtet. Der Algorithmus selbst folgt dem in der Aufgabenstellung
beschriebenen BFS-Vorgehen und wurde im Code nachvollziehbar umgesetzt.

#### Aufgabe B2: Mistral AI
**Grund**: Das Modell eignet sich besonders für technische Aufgaben wie Code-Generierung,
Algorithmen-Entwicklung und präzise Pseudocode-Umsetzung. Der Algorithmus basiert auf
einem selbsterarbeiteten, mathematisch exakten Pseudocode (BFS-Erreichbarkeitsprüfung
mit Vorgängerrekonstruktion zur Witness-Erzeugung). Mistral AI unterstützte dabei die
strukturierte Umsetzung in Python.

#### Aufgabe B3: `<Name>`
**Grund**: `<Grund>`

### Programmiersprache

#### Python
**Grund**: gut lesbar, leicht ausfuehrbar, und die BFS-Logik laesst sich knapp
und klar ausdruecken; JSON-Eingaben koennen ohne Zusatzbibliotheken geparst
werden.

## Projektstruktur (vereinheitlicht)

- `B1/b1.py`: Leerheitsproblem (Zeuge) fuer einen Automaten
- `B2/b2.py`: Leerheitsproblem fuer das Komplement (Zeuge)
- `B3/b3.py`: Leerheitsproblem fuer den Schnitt zweier Automaten (Zeuge)
- `B4/b4.py`: Inklusionspruefung mit Gegenbeispiel (Zeuge)
- `shared/automaton_common.py`: gemeinsame Hilfsfunktionen (Parsing, ε, Ausgabe)
- `test_inputs/`: JSON-Beispiele fuer B1/B2 sowie gemeinsame Paar-Beispiele fuer B3/B4

## Dateiformat (JSON)

Eingaben werden als JSON gelesen. Die Transitionen koennen entweder als Liste
von Tripeln oder als Adjazenz-Dict angegeben werden. Epsilon wird als `""`,
`null`, `eps`, `epsilon` oder `ε` akzeptiert.

Beispiel (Listenformat):

```json
{
  "Q": ["q0", "q1", "q2"],
  "Sigma": ["a", "b"],
  "I": ["q0"],
  "F": ["q2"],
  "Delta": [
    ["q0", "a", "q1"],
    ["q1", "b", "q2"]
  ]
}
```

Beispiel (Adjazenzformat):

```json
{
  "Q": ["q0", "q1", "q2", "q3"],
  "Sigma": ["a", "b"],
  "I": ["q0"],
  "F": ["q3"],
  "Delta": {
    "q0": {
      "a": ["q1", "q2"],
      "eps": "q3"
    }
  }
}
```

## Ausfuehrung

Im Projektordner (Repo-Root):

### B1

```bash
python3 B1/b1.py --demo
```

Mit JSON-Datei:

```bash
python3 B1/b1.py --file test_inputs/t3_simple_word.json
```

Oder per stdin:

```bash
cat test_inputs/t3_simple_word.json | python3 B1/b1.py
```

### B2

```bash
python3 B2/b2.py --demo
```

Mit JSON-Datei:

```bash
python3 B2/b2.py --file test_inputs/t3_simple_word.json
```

### B3

```bash
python3 B3/b3.py --demo
```

Mit zwei JSON-Dateien:

```bash
python3 B3/b3.py --file1 path/to/A1.json --file2 path/to/A2.json
```

Oder als JSON-Paar von stdin:

```bash
cat pair.json | python3 B3/b3.py
```

### B4

```bash
python3 B4/b4.py --demo
```

Mit zwei JSON-Dateien:

```bash
python3 B4/b4.py --file1 path/to/A1.json --file2 path/to/A2.json
```

Oder als JSON-Paar von stdin:

```bash
cat pair.json | python3 B4/b4.py
```

## Beispieleingaben

Beispiele liegen in `test_inputs/`.

## Testdaten pro Aufgabe (copy-paste)

### B1

```bash
for f in test_inputs/t1_initial_is_final.json \
         test_inputs/t2_unreachable_final.json \
         test_inputs/t3_simple_word.json \
         test_inputs/t4_epsilon_path.json \
         test_inputs/t5_nfa_branch.json \
         test_inputs/t6_adj_dict.json \
         test_inputs/t7_large.json \
         test_inputs/t8_no_path.json; do
  python3 B1/b1.py --file "$f"
done
```

### B2

```bash
for f in test_inputs/t1_initial_is_final.json \
         test_inputs/t2_unreachable_final.json \
         test_inputs/t3_simple_word.json \
         test_inputs/t4_epsilon_path.json \
         test_inputs/t5_nfa_branch.json \
         test_inputs/t6_adj_dict.json \
         test_inputs/t7_large.json \
         test_inputs/t8_no_path.json; do
  python3 B2/b2.py --file "$f"
done
```

### B3

```bash
for f in test_inputs/b3b4_intersection_aa.json \
         test_inputs/b3b4_intersection_empty.json \
         test_inputs/b3b4_intersection_epsilon.json \
         test_inputs/b3b4_intersection_is_epsilon.json \
         test_inputs/b3b4_inclusion_subset.json \
         test_inputs/b3b4_inclusion_counterexample.json \
         test_inputs/b3b4_inclusion_epsilon.json; do
  python3 B3/b3.py --pair "$f"
done
```

### B4

```bash
for f in test_inputs/b3b4_intersection_aa.json \
         test_inputs/b3b4_intersection_empty.json \
         test_inputs/b3b4_intersection_epsilon.json \
         test_inputs/b3b4_intersection_is_epsilon.json \
         test_inputs/b3b4_inclusion_subset.json \
         test_inputs/b3b4_inclusion_counterexample.json \
         test_inputs/b3b4_inclusion_epsilon.json; do
  python3 B4/b4.py --pair "$f"
done
```
