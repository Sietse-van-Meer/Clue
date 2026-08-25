#Objective 2: Creating the secret envelope.
#This envelope consists the answer of the game, who did the murder, with what weapon, and at what place?
#The secret envelope consists of randomly 1 suspect, 1 weapon, and 1 room.

#1.1 Make a secret envelope
import random


#Import lists from exercise 1

suspects = ["Green", "Mustard", "Peacock", "Plum", "Scarlett", "White"]
weapons = ["candlestick", "dagger", "lead piping", "revolver", "rope", "spanner"]
rooms = ["ballroom", "billiard room", "conservatory", "dining room", "hall", "kitchen", "library", "lounge", "study"]

#I know random.choice to choose a random object from a list.
#Idea 1, just like the merge from exercise 1, to make a new list, we can use + to add the choices to make one new list, the envelope.
#envelope = random.choice(suspects) + random.choice(weapons) + random.choice(rooms)

#Idea 2, make a lists from the random choices
#envelope = [random.choice(suspects), random.choice(weapons), random.choice(rooms)]

#Check the envelope to see if it works
#print(envelope)

#It returns Peacockrevolverstudy. This is not what I want, I want [Peacock, revolver, study]
#Idea 2 works, hooray!


#1.2 Think about, why use a list, why not a dictionary or a tuple?
#Then I have to think about how to save the three cards
#A list: can have duplicates and information can be changed. Lists are ordered

#A dictionary: Combines keys with values -> could be {suspect: Peacock, weapon: revolver, room: study}. This could be a good fit to tell the code to choose one 
# of each category. Dictionaries are ordered.

#A tuple: Cannot be altered (immutable), but can contain duplicates. I think this could also work, given that the secret envelope should never change for a game. 
#Tuples are also ordered.

#My understanding is that each of these ideas could work. Lists seem the most flexible, tuples force characteristics that inherently part of the envelope (immutable). 
#Still, I think a dictionary would be the most accurate solution. So you can confirm one item from each list is selected.
#That makes prints like suspect Plum, weapon: rope, room: kitchen easier as well. 

#Idea 3, make a dictionary
#We overwrite envelope and print it.
envelope = {"Suspect": random.choice(suspects), "Weapon": random.choice(weapons), "Room": random.choice(rooms)}
#print(envelope)


#1.3 Why do we use random? 
    #Well, we want to make a random choice from a list of cards.
#1.4 What is the difference between random.choice() and random.shuffle(). 
    #Shuffle shuffles a list randomly, choice chooses a card randomly.
#1.5 Why do we take one card from each category, could we not take three cards from total_cards (see exercise 01). 
    #In the big list, we do not know what card belongs to what category. By randomly choosing 3 cards from the total_list we could end up taking 2 rooms and 1 suspect 
    #for example. That is not what we want.

#Final answer: 
print(f"Secret envelope: {envelope}")

#Covered in this piece of code: lists, tuples, dictionaries, f strings, random.choice(), random.shuffle().

#AI review: 