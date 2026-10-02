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

### Exercise 01 — Card system 
Created the three Clue card categories and combined them into one list.

### Exercise 02 — Secret envelope 
Randomly selected one suspect, one weapon, and one room and stored them in a dictionary.

### Exercise 03 — Remove envelope cards 
Created the playable deck by excluding the three cards in the secret envelope.


### Exercise 04 — Shuffle the deck 
Randomized the order of the remaining cards while preserving the deck contents.

### Exercise 05 — Deal cards 
Dealt cards to players in turn and explored both modulo-based and nested-loop solutions.

### Exercise 06 — Generalize players and hands 
Replaced hardcoded player hands with a dictionary and made the dealing logic work for 3–6 players.

### Exercise 07 — Suggestions 
Built the first suggestion mechanic using one suspect, one weapon, and one room.

### Exercise 08 — Find possible disprovers 
Checked which players could disprove a suggestion by holding at least one suggested card.

### Exercise 09 — Correct turn order 
Made players disprove in the correct clockwise order and stopped after the first valid disprover.

### Exercise 10 — Reveal one disproving card 
Made the first disproving player reveal one matching card and returned both the disproving player and shown card.

### Exercise 11 — Store shown-card knowledge 
Created player-specific knowledge structures and stored confirmed cards that were privately shown.

### Exercise 12 — Store NOT HAVE knowledge 
Added negative knowledge for players who cannot disprove a suggestion.

Players now distinguish between cards another player definitely **HAS** and definitely **DOES NOT HAVE**.

Public and private information are treated differently:
- Everyone learns when a player cannot disprove.
- Only the suggesting player learns the exact shown card.

### Exercise 13 — Store uncertain knowledge 

Add a third type of knowledge for situations where a player disproves a suggestion but the observer does not see the shown card.

Example:

```text
Player 3 has at least one of:
{Green, rope, study}
```

These one-of constraints must remain grouped so they can later be reduced using HAVE and NOT HAVE information.

### Exercise 14 — Deduce from uncertain knowledge

Use existing HAVE and NOT HAVE information to reduce one-of constraints.

For example:

```text
Player 3 has at least one of:
{Green, rope, study}

Player 3 does NOT have:
Green
study
```

Therefore:

```text
Player 3 HAS rope
```

Exercise 15 — Deduce using player hand sizes

Use the fixed number of cards in each player's hand as an additional deduction constraint.
If an observer already knows all cards in another player's hand, every remaining card can be marked as NOT HAVE. This information can then trigger further deductions through the existing knowledge engine.


## Long-term goal

Gradually build toward:

- Complete suggestion and disproving logic
- Envelope candidate tracking
- A complete playable game loop
- CPU strategies
- Simulations and strategy comparison
