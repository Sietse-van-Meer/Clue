#Exercise 6: Generalize players and hands. 
#Currently we use 3 players and lists. Now we make a big step and use dictionaries and n umber of players (between 3 and 6)

#Let's start using dictionaries for both, that is more convenient.



#From previous exercises
import random

suspects = ["Green", "Mustard", "Peacock", "Plum", "Scarlett", "White"]
weapons = ["candlestick", "dagger", "lead piping", "revolver", "rope", "spanner"]
rooms = ["ballroom", "billiard room", "conservatory", "dining room", "hall", "kitchen", "library", "lounge", "study"]
total_cards = suspects + weapons + rooms

#Envelope
envelope = {"Suspect": random.choice(suspects), "Weapon": random.choice(weapons), "Room": random.choice(rooms)}
in_envelope_cards = list(envelope.values())


#The deck
deck = [x for x in total_cards if x not in in_envelope_cards]
#print(len(deck))

#Shuffled deck
shuffled_deck = random.sample(deck, len(deck))
#print(shuffled_deck)
#print(len(shuffled_deck))

#6.1 Create the hands for n players (between 3 and 6) in a dictionary.

#Using random.randint we can print a random number between 3 and 6 
number_of_players = random.randint(3,6)
print(number_of_players)

#Now we need a loop to make a dictionary of hands
hands = {}
i=0
while i < number_of_players:
    hands.update({f'Player {i+1}':[]})
    i += 1

#print(hands)
#Comparing number_of_players to players list seems good, it works!
#So for lists we use .append() and for dictionaries we use .update()
#Also not that we use player i+1 in the f string, since I started the loop from 0.
#See https://www.w3schools.com/python/python_dictionaries_add.asp.



#6.2 Deal using the dictionary

#I think we again have to go and combine the while and for loop to combine 
#the total amount of cards with the keys in the dictionary (the players).
i = 0
while i < len(shuffled_deck):
    for key,value in hands.items():  #keys and values
        if i < len(shuffled_deck):
            value.append(shuffled_deck[i])
            i += 1

print(hands)

#At first I thought it didn't work, but it only gave errors when the index goes out of bounds.
#That is, the last round of dealing did not contain enough cards for all players.
#For example, with 5 players, and 18 cards (21-3 envelope cards):
    #Only 3 players can get 4 cards, the last two players get only 3.

#Checks:
#1. 18 cards are dealt in total
#https://stackoverflow.com/questions/17133000/obtaining-length-of-list-as-a-value-in-dictionary-in-python-2-7

lengths = {key:len(value) for key,value in hands.items()}
#Sum over the values
#https://stackoverflow.com/questions/4880960/how-to-sum-all-the-values-in-a-dictionary
print(sum(lengths.values()))

#2. Every player has a hand, check. This comes from the code already looping over the players 
#to hand out cards one by one.
#print(hands)

#3. No envelope card appears in any hand
#I needed a hint here, because using list comprehension I could not get it done.
#The hint was using a for loop. 
matches = []
for hand in hands.values():
    for card in hand:
        if card in in_envelope_cards:
            matches.append(card)

print(matches)
#I ran into various problems with this check. 
# I either continuously remade the matches list in the loop, or made a generator object using .append().
#In the end, I used a nested loop, list comprehension could work with .extend().

#.extend() vs .append(): https://stackoverflow.com/questions/252703/what-is-the-difference-between-pythons-list-methods-append-and-extend
# Use .append() to add an element to a list
# Use .extend() to concatenate the first list with another list/iterable.

#4. No card has been dealt twice
cards_dealt = []

for hand in hands.values():
    for card in hand:
        cards_dealt.append(card)

#Return duplicates 
cards_dealt_twice = [card for card in cards_dealt if cards_dealt.count(card) > 1]
print(cards_dealt)
print(cards_dealt_twice)
#Seems to work as well!

#5. The same code works for 3-6 players, check (run the code multiple times)

#This concludes exercise 6.

#Topics covered in this piece of code: while and for loops, dictionaries, lists, list comprehension, random.randint(), 
#remove hardcoding, .append() vs .extend()

#AI: 
    #In check 3, I mistakenly used envelope, instead of in_envelope cards in check 3. 
    #Essentially comparing suspect, weapon, room instead of the cards.

    #In check 4, the list comprehension line for cards dealt twice does not work, due to that card is a string.
    #So if card = 'rope', then card.count(card) means "rope".count("rope). Which is always one.
    #I want to ask how often does the card occur in whole cards_deal list.

    #Possibly, in the future, it would be easier to check for the uniqueness and count this, rather than return no duplicates.
    #Returning 'nothing' can be done in various ways. Code could look good, but not work as intended.
