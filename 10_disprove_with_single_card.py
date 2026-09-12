#Exercise 10: Reveal one card when disproving a suggestion, rather than the whole list.
#Using the turn-order logic from exercise 9,
#the goal is now to let the first player who can disprove reveal exactly one card.

#In real Clue, a player may have multiple cards that match the suggestion.
#However, that player only shows one of those cards to the suggesting player.


#From previous exercises
import random

suspects = ["Green", "Mustard", "Peacock", "Plum", "Scarlett", "White"]
weapons = ["candlestick", "dagger", "lead piping", "revolver", "rope", "spanner"]
rooms = ["ballroom", "billiard room", "conservatory", "dining room", "hall", "kitchen", "library", "lounge", "study"]
total_cards = suspects + weapons + rooms


#Envelope
envelope = {
    "Suspect": random.choice(suspects),
    "Weapon": random.choice(weapons),
    "Room": random.choice(rooms)
}

in_envelope_cards = list(envelope.values())


#The deck
deck = [x for x in total_cards if x not in in_envelope_cards]


#Shuffled deck
shuffled_deck = random.sample(deck, len(deck))


#Random number of players between 3 and 6
number_of_players = random.randint(3,6)


#Make player hands
hands = {}

i = 0
while i < number_of_players:
    hands.update({f'Player {i+1}': []})
    i += 1


#Deal the cards
i = 0

while i < len(shuffled_deck):
    for key, value in hands.items():
        if i < len(shuffled_deck):
            value.append(shuffled_deck[i])
            i += 1


#Make suggestion
suggestion_player = random.choice(list(hands.keys()))

suggestion = {
    "Suspect": random.choice(suspects),
    "Weapon": random.choice(weapons),
    "Room": random.choice(rooms)
}

suggestion_cards = list(suggestion.values())
players_in_game = list(hands.keys())

#For debugging purposes:
# def check_hands():
#     disprove_cards = {}
#     print(f'DEBUGGING: {suggestion_player} suggests: {suggestion_cards}')
#     for player in players_in_game:
#         if player != suggestion_player:
#             matches = [x for x in hands[player] if x in suggestion_cards] #list(hands[player]) = hands[player] when using in!
#             if matches:
#                 disprove_cards[player] = matches

#     for player in hands.keys():
#         if player != suggestion_player:
#             if player in disprove_cards:
#                 print(f'DEBUGGING: {player} can disprove with {disprove_cards[player]}')
#             else:
#                 print(f'DEBUGGING: {player} cannot disprove')

# check_hands()


#Exercise 10: In exercise 9, we mainly printed who could disprove.
#Now we want to STORE this information because we will need it later.

#What to do:
#1. Store disproving_player
#2. Store shown_card
#3. Stop checking other players when a card is shown

#Expected output example:

#Player 2 suggests: ['Mustard', 'rope', 'study']

#Checking Player 3
#Player 3 cannot disprove

#Checking Player 4
#Player 4 can disprove

#Player 4 shows Player 2: rope


#Another possible result:

#Player 2 suggests: ['Mustard', 'rope', 'study']

#Checking Player 3
#Player 3 cannot disprove

#Checking Player 4
#Player 4 cannot disprove

#Checking Player 1
#Player 1 cannot disprove

#Nobody could disprove the suggestion.

suggestion_player_index = players_in_game.index(suggestion_player)
players_after_suggesting_player_loop = players_in_game[suggestion_player_index + 1:]
players_before_suggesting_player_loop =  players_in_game[:suggestion_player_index]
empty_list = []

players_outside_of_suggestion_player = players_after_suggesting_player_loop + players_before_suggesting_player_loop

def suggestion_output():
    print(f'{suggestion_player} suggests: {suggestion_cards}')
    for q in players_outside_of_suggestion_player: 
            print(f'Checking {q}')
            matches = [x for x in hands[q] if x in suggestion_cards]
            
            if matches != empty_list:
                disproving_player = q
                shown_card = random.choice(matches)
                print(f'{disproving_player} shows {suggestion_player}: {shown_card}')
                return disproving_player, shown_card
            elif matches == empty_list:
                print(f'{q} cannot disprove')

    if matches == empty_list:
        disproving_player = None
        shown_card = None
        print("Nobody could disprove this suggestion")
        return None, None
    

disproving_player, shown_card = suggestion_output()

print(shown_card)




#Additional questions:

#Why do we store disproving_player and shown_card?
#First, we can use it as knowledge for deduction.
#Second, we can use disproving_player and shown_card as general part of logging later in the process of building Clue.

#Why do we store shown_card instead of only printing the card?
#We can use shown_card as part of logging of the game later in the process of building Clue.

#Why do we first calculate all matching cards before choosing one?
#Because there could be one or more matching cards. And, if multiple cards can be shown, the player could choose which one to share!

#What should disproving_player and shown_card contain if nobody can disprove?
#It's fine to just return None such that you see in the output variables that no card is shown and nobody could disprove.

#Topics covered in this piece of code:
#None, storing results, random.choice(), break, turn-order logic, list comprehension, return


#AI:
#I made a superfluous special case, since random.choice() would work if matches has length 1 or more.
#Second, I made a function, but the function should return disproving_player and shown_card!