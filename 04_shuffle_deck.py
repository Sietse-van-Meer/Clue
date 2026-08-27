#Exercise 4: Shuffle the deck.

#Now that we got our deck and envelope (see exercise 3), we should shuffle the deck before dealing the cards.

import random

#The lists of initial cards
suspects = ["Green", "Mustard", "Peacock", "Plum", "Scarlett", "White"]
weapons = ["candlestick", "dagger", "lead piping", "revolver", "rope", "spanner"]
rooms = ["ballroom", "billiard room", "conservatory", "dining room", "hall", "kitchen", "library", "lounge", "study"]
total_cards = suspects + weapons + rooms


#Envelope
envelope = {"Suspect": random.choice(suspects), "Weapon": random.choice(weapons), "Room": random.choice(rooms)}
in_envelope_cards = list(envelope.values())

#The deck
deck = [x for x in total_cards if x not in in_envelope_cards]

print(f'Initial deck: {deck}')
#4.1 Shuffle the deck

#Idea 1: Use random.shuffle()
#shuffled_deck = random.shuffle(deck)
#print(f'Shuffled deck: {shuffled_deck}')
#This results in Shuffled deck: None. Clearly it does not what I thought it did.

#I see, in the documentation, they don't really make a new variable: https://www.geeksforgeeks.org/python/random-shuffle-function-in-python/
#And for this case, that also does not seem to be necessary. Let's try a new shuffle.

random.shuffle(deck)
print(f'New deck order: {deck}')

#That seemed to work. So in order to shuffle the deck, use random.shuffle(deck), and you are ready to hand out a shuffled deck.


#4.3 How is it different from random.sample().
#Well, in the documentation, random.sample() takes a random sample from a list. 
#We could do: 
#sampled_deck = random.sample(deck,3)
#and we would sample 3 random entries from the deck list. The use is different than random.shuffle().

#4.4 How to keep the unshuffled list
#Now I look into documentation how to keep the original list.
# Surprisingly, it is a use case for random.sample(): https://stackoverflow.com/questions/47750757/how-to-shuffle-a-copied-list-without-shuffling-the-original-list
#By using random.sample(list, len(list)), you randomly sample from your earlier list, essentially also shuffling the list.
#And with random.sample() you CAN define a new variable as original and shuffled deck

print(f'Current deck order: {deck}')
newly_shuffled_deck = random.sample(deck, len(deck))
print(f'Newly shuffled deck order: {newly_shuffled_deck}')
print(f'Once more the original deck order to double check: {deck}')

if len(deck) == len(newly_shuffled_deck):
    print('The length is equal as expected')

different_cards_in_deck_and_shuffled_deck = [x for x in deck if x not in newly_shuffled_deck]
print(different_cards_in_deck_and_shuffled_deck)
#If the print is an empty list, then the cards are correctly shuffled and the values in the two lists are the same. 
#(only the order is different)

#That works! That is a way to keep both the orignal and shuffled list.

#4.5 Why do we shuffle before dealing the cards
#Because then, after shuffling, we can conveniently deal cards from the list one by one, without calling the randomized choice 
#function in every draw and then subsequently omitting this card from the list. This shuffling once, seems efficient for dealing cards. 
#Moreover, next to the repeated random.choice() actions, we also have to remove these cards from the list before drawing again to avoid drawing the same card twice.
#This extra action may not be necessary if you can go through the list in order (if the cards are in random order).

#Topics covered in this piece of code: random.shuffle, random.sample(), list comprehensions, if statement.

#AI review: Don't forget to check if the cards in the shuffled list and original list are the same (List comprehensions). 
#Also going over the list in order seems to be an efficient way to deal out cards randomly (if the cards are in random order). With
#random.choice() you should remove the card before choosing a card from the list again. The latter is slightly less efficient/beautiful.