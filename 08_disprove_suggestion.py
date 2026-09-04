#Exercise 8, disprove a suggestion.
#Using the player hands from exercise 6 and suggestion from exercise 7
#the goal is now to disprove the suggestion.

#From previous exercises
import random

suspects = ["Green", "Mustard", "Peacock", "Plum", "Scarlett", "White"]
weapons = ["candlestick", "dagger", "lead piping", "revolver", "rope", "spanner"]
rooms = ["ballroom", "billiard room", "conservatory", "dining room", "hall", "kitchen", "library", "lounge", "study"]
total_cards = suspects + weapons + rooms

#Envelope
envelope = {"Suspect": random.choice(suspects), "Weapon": random.choice(weapons), "Room": random.choice(rooms)}
in_envelope_cards = list(envelope.values())
print(f'Cards in envelope: {in_envelope_cards}')

#The deck
deck = [x for x in total_cards if x not in in_envelope_cards]
#print(len(deck))

#Shuffled deck
shuffled_deck = random.sample(deck, len(deck))

#Using random.randint we can print a random number between 3 and 6 
number_of_players = random.randint(3,6)
#print(number_of_players)

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

print(f'Cards in hands: {hands}')

#Make suggestion
suggestion_player = random.choice(list(hands.keys()))
suggestion = {"Suspect":random.choice(suspects), "Weapon": random.choice(weapons), "Room": random.choice(rooms)}

def make_rumor():
    print(f'{suggestion_player} makes a suggestion')
    print(f'Suspect: {suggestion["Suspect"]}')
    print(f'Weapon: {suggestion["Weapon"]}')
    print(f'Room: {suggestion["Room"]}')

#We print the result 
#make_rumor()


#8.1 Get the suggestion cards such that we can easily compare them to player's hand cards.
suggestion_cards = list(suggestion.values())
#print(suggestion_cards)
#I choose a list, because to disprove a suggestion, we need to disprove one of the three cards.
#The category is not that relevant anymore for this part.


#8.2 Check every other player's hand
players_in_game = list(hands.keys())



#IDEA 1: nice, but it creates many dictionaries rather than 1
#def check_hands():
#    for player in players_in_game:
#        if player != suggestion_player:
#            disprove_cards = {player: [x for x in list(hands[player]) if x in suggestion_cards]}
#            print(disprove_cards)

#IDEA 2: Try to first define the empty dictionary and fill it with matching cards for the player.
#Then you can get one big dictionary.


def check_hands():
    disprove_cards = {}
    print(f'{suggestion_player} suggests: {suggestion_cards}')
    for player in players_in_game:
        if player != suggestion_player:
            matches = [x for x in hands[player] if x in suggestion_cards] #list(hands[player]) = hands[player] when using in!
            if matches:
                disprove_cards[player] = matches

    for player in hands.keys():
        if player != suggestion_player:
            if player in disprove_cards:
                print(f'{player} can disprove with {disprove_cards[player]}')
            else:
                print(f'{player} cannot disprove')

check_hands()

#Additional questions:
    #How do you skip the suggesting player in the loop: using if statement with player != suggestion_player
    #How can you find the overlap between a player's hand and the suggestion: Using list comprehension
    #Why do we store all matching cards rather than immediately picking one: Since this is still a concept version of the game, in which 
    #we attempt to get a good grip on all cards to disprove a rumor. The order etcetera will come later. In real clue, and in our
    #later versions, if multiple players can disprove, only the first eligible player will do by revealing one card to the 
    #suggesting player.

#Topics covered in this piece of code: functions, if statements, list comprehension, dictionary access

#AI: 
#My idea 1 made many dictionaries. Using one dictionary is more organized Is to use later to disprove a suggestion in order.
#Put the empty dictionary, inside the check_hands (did not change the correctness, but is cleaner)