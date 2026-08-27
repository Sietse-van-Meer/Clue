#Exercise 3: Remove the envolpe cards from the deck

#libraries
import random 


#We now have from exercise 1
suspects = ["Green", "Mustard", "Peacock", "Plum", "Scarlett", "White"]
weapons = ["candlestick", "dagger", "lead piping", "revolver", "rope", "spanner"]
rooms = ["ballroom", "billiard room", "conservatory", "dining room", "hall", "kitchen", "library", "lounge", "study"]
total_cards = suspects + weapons + rooms


#And from exercise 2
envelope = {"Suspect": random.choice(suspects), "Weapon": random.choice(weapons), "Room": random.choice(rooms)}
#print(envelope)

#2.1 create a new list, deck that contains all cards from total_cards except the cards that are part of the envelope.
#The final result should print something like 
#Total cards: 21
#Envelope cards: 3
#Cards available for dealing: 18

#Idea 1: Go through the values in a dictionary using a for loop. We have to use .values() to get the values from a dictionary.
#This worked, but the for loop returned the values below each other rather than in a list.
#for i in envelope.values():
#    print(i)

#Idea 2: I need to make a list using list().
#Luckily I found a stackoverflow post: https://stackoverflow.com/questions/1679384/converting-dictionary-to-list
in_envelope_cards = list(envelope.values())
#print(list(envelope.values()))


#Then now, how to go over each card in total_cards, and remove the cards that match the envelope.

#This way, we make the deck. I found on stackoverflow one way using sets.
#The downside is that using sets, the order of elements are not preserved, and duplicates within lists are deleted. 
#Since the side effects seem not to affect our case, I gave it a try. It works.

#However, translating to sets kind of increases data types. Possibly, there is a way using just lists and dictionaries.
#I found here: https://www.geeksforgeeks.org/python/python-remove-all-values-from-a-list-present-in-other-list/ another way.
#This seems to be list comprehension: a shorter syntax when you want to create a new list based on the values of an existing list.
deck = [x for x in total_cards if x not in in_envelope_cards]
#print(deck)

#Check if the envelope cards are no longer present in deck. 
# So check for duplicates between deck and in_envelope_cards.

matches = [x for x in deck if x in in_envelope_cards]
#print(matches)


#We seem to have found our answers here. 
#Still I feel that sets are actually very handy when dealing with situations where there are no duplicates (like ours).
#Sets seem to be easily subtracted, compared. Now I used list comprehension, also fine I think.

print(f'total cards: {len(total_cards)}')
print(f'Envelope cards: {len(in_envelope_cards)}')
print(f'Cards available for dealing: {len(deck)}')
print(f'Matches between cards available for dealing and envelope cards: {len(matches)}')


#Topics covered in this piece of code: List comprehensions, dictionary.values(), dictionary.keys(), dictionary.items(), f strings.

#AI review: It is good. Remember the differences between dictionary.values(), dictionary.keys(), and dictionary.items().