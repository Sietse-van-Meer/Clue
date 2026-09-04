#E7, a player makes a suggestion.

#Goal:
    #Suggestion consists of 
    #1 suspect
    #1 weapon
    #1 room

#Example: Player 2 suggests: Plum / rope / kitchen


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

#Using random.randint we can print a random number between 3 and 6 
number_of_players = random.randint(3,6)
print(number_of_players)

#Now we need a loop to make a dictionary of hands
hands = {}
i=0
while i < number_of_players:
    hands.update({f'Player {i+1}':[]})
    i += 1


i = 0
while i < len(shuffled_deck):
    for key,value in hands.items():  #keys and values
        if i < len(shuffled_deck):
            value.append(shuffled_deck[i])
            i += 1

#print(hands)


#7.1 pick one player randomly to make a suggestion (for now)
suggestion_player = random.choice(list(hands.keys()))
print(suggestion_player)

#So we knew from before random.choice() is what one can use to randomly choose from a list.
#But how to get one element from the dictionary. Well, I looked it up on
#https://stackoverflow.com/questions/4859292/how-can-i-get-a-random-key-value-pair-from-a-dictionary
#I found we had to make list(hands.keys()) to make it work.
#Unlike random.choice([hands.keys()]), which returned dict_keys(['Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5'])
#That makes me wonder why list() and [] are different. Similar to {} and dict().
#Possibly it is because list(iterable) unpacks or converts an iterable into a list. 
#For example, list('abc') results in ['a', 'b', 'c'].
#[item] creates a list containing the exact item as a single element. For example, ['abc'] results in ['abc']. 



#7.2 Create the suggestion, by randomly selecting one item from suspects, one from weapons, and one item from rooms.
suggestion = {"Suspect":random.choice(suspects), "Weapon": random.choice(weapons), "Room": random.choice(rooms)}
print(suggestion)

#I again choose a dictionary, such that we get the practical layout: {suspect: random_suspect, weapon: random_weapon, room: random_room}


#7.3 Print suggestion: 
#Player 3 makes a suggestion:
#Suspect: 
#Weapon:
#Room


def make_rumor():
    print(f'{suggestion_player} makes a suggestion')
    print(f'Suspect: {suggestion["Suspect"]}')
    print(f'Weapon: {suggestion["Weapon"]}')
    print(f'Room: {suggestion["Room"]}')

#We print the result 
make_rumor()

#Another use of f strings again. I had to look up again how to exactly return the value of a key in the dictionary.
#dict["key"] returns the value. See https://stackoverflow.com/questions/5904969/how-to-print-a-dictionarys-key.



#7.4 Validate it
#Check if suspect, weapon, room really belong to their corresponding lists and the suggesting player exists in hands.
#Using list comprehension we can check whether Peacock is also part of suspects (it is of course).
#One can extend this method to weapons and rooms, but it seems good and working as planned.


#IDEA 1 (WRONG)
#suspect_matches = [x for x in suspects if x in suggestion["Suspect"]]
#print(suspect_matches)

#IDEA 2 (RIGHT)
suspect_in_suspects = suggestion["Suspect"] in suspects
weapon_in_weapons = suggestion["Weapon"] in weapons
room_in_rooms = suggestion["Room"] in rooms
player_in_players = suggestion_player in hands #For dictionaries, in check the keys by default!!
print(f'Suspect check: {suspect_in_suspects}')
print(f'Weapon check:{weapon_in_weapons}')
print(f'Room check: {room_in_rooms}')
print(f'Player check: {player_in_players}')

#Extra questions:
#What data structure to choose for suggestion, and why?
#I use the dictionary structure, since one can easily organize and index the right objects in this structure.

#How do you randomly select a player from the keys of a dictionary?
#I made a list from the players and then randomly chose one from the list. In code: random.choice(list(hands.keys()))

#Why do we still select one card from each category separately?
#Because we clearly want to separate categories to ensure we choose one card of each category.

#Can a plyaer suggest a card that is already in their own hand?
#In current code, yes that is possible. The suggestion is completely random from the suspects, weapons, and rooms list.

#Can a player accidentally suggest the actual envelope combination?
#Yes that is possible, though that chance is small. If one would choose completely randomly (excluding even you own handcards)
#The chance is 1/(6*6*9) = 1/324 if cards are drawn uniformly from all combinations.

#Topics covered in this piece of code: random.choice, dictionary access, functions, membership checks, booleans

#AI: 
#I used list comprehension to check whether a string (like a suspect, Mustard) appears in a list.
#But apparently, one can more efficiently check using: suggestion["suspect"] in suspects, and return a boolean (TRUE/FALSE).
#Using in we automatically take keys, so 
#player_in_players = suggestion_player in list(hands.keys()) 
# can become
#player_in_players = suggestion_player in hands