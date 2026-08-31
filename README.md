# Clue From Scratch 🕵️

A Python learning project in which I build **Clue (Cluedo) from scratch**, one exercise at a time.

The goal is to understand the code well enough to explain and modify it myself.

## Approach

For each exercise:

1. I solve the problem myself.
2. I document my reasoning and attempts.
3. AI reviews the finished code afterwards.
4. Each exercise is saved separately to show the progression of the project.

## Progress

### Exercise 01 — Card system ✅
Created the three Clue card categories and combined them into one list.

Practiced: lists, variables, combining lists, `len()`, f-strings.

### Exercise 02 — Secret envelope ✅
Randomly selected one suspect, one weapon, and one room and stored them in a dictionary.

Practiced: `random.choice()`, lists, tuples, dictionaries, dictionary keys and values.

### Exercise 03 — Remove envelope cards ✅
Created the playable deck by excluding the three cards in the secret envelope.

Practiced: list comprehensions, membership checks, dictionary `.values()`.

### Exercise 04 — Shuffle the deck ✅
Randomized the order of the remaining cards while preserving the deck contents.

Practiced: `random.shuffle()`, `random.sample()`, list validation.

### Exercise 05 — Deal cards ✅
Dealt cards to three players in turn and explored both modulo-based and nested-loop solutions.

Practiced: `enumerate()`, modulo `%`, `if/elif/else`, `while` loops, nested loops, `.append()`.

### Exercise 06 — Generalize players and hands ✅
Replaced hardcoded player hands with a dictionary and made the dealing logic work for 3–6 players.

Practiced: dictionaries, dynamic data structures, nested loops, `random.randint()`, reducing hardcoding, validation checks.

## Next

### Exercise 07 — Suggestions

Build the first Clue suggestion mechanic using:

- one suspect
- one weapon
- one room
- a player making the suggestion

This will be the first step toward checking whether another player can disprove a suggestion.

## Long-term goal

Gradually build toward:

- Suggestions and disproving
- Knowledge tracking
- Deduction rules
- CPU strategies
- Simulations
- Testing and refactoring
