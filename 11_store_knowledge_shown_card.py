#Exercise 11: Store knowledge from a shown card
#Using the result from exercise 10, the goal is now to record what the suggesting player learns after another player shows a card.


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




#Exercise 11:
#Now we want to record the information that the suggesting player learned.

#If Player 4 showed "rope" to Player 2,
#Player 2 now knows that Player 4 HAS rope.

#For now, we only store confirmed cards that were actually shown.

#We are not yet storing:
#- cards players definitely do not have
#- uncertain information
#- envelope possibilities


#11.1 Create a knowledge structure
#11.2 Store the own hand
#11.3 Store the shown card (avoid duplicates)
#11.4 Print current knowledge


#Example output:

#Player 2 knowledge:

#Player 1: []
#Player 2: ['Green', 'dagger', 'hall']
#Player 3: []
#Player 4: ['rope']


#I thought of using nested dictionary with a list as values for cards in the hand. 

#IDEA 1 (WRONG!)
# player_knowledge = {}
# child_knowledge = {}

# for i in players_in_game:
#     for j in players_in_game:
#         child_knowledge[i] = []
#         player_knowledge[i] = child_knowledge

#I created the child knowledge once, rather than in the loop and using j. As a consequence all players pointed to the same dictionary and all the players 
#information was printed even though I thought to point to player 1 = player 1 in the the following k == l loop.

#IDEA 2: Create the child_knowledge dictionary in the loop!
#Empty knowledge scheme


#Find first disproving player and reveal one card

def game_simulation(turns):

    def suggestion_output():
        print(f'Player {starting_player_index+1} turn.  Player {starting_player_index+1} suggests: {suggestion_cards}')
        for q in players_outside_of_suggestion_player: 
                print(f'Checking {q}')
                matches = [x for x in hands[q] if x in suggestion_cards]
                
                if matches:
                    disproving_player = q
                    shown_card = random.choice(matches)
                    print(f'{disproving_player} shows player {starting_player_index + 1}: {shown_card}')
                    player_knowledge[f'Player {starting_player_index+1}'][q].add(shown_card)  #Link starting_player_index to keys in player_knowledge, and sets can't have duplicates.
                    return disproving_player, shown_card
                else:
                    print(f'{q} cannot disprove')

        print("Nobody could disprove this suggestion")
        return None, None #Return nothing

    #Initial knowledge is player_knowledge
    #Make correct checking order

    #Initial knowledge 
    players_in_game = list(hands.keys())

    #Randomly choose the first player
    starting_player = random.choice(list(hands.keys()))

    player_knowledge = {}
    child_knowledge = {}
    

    for i in players_in_game:    
                child_knowledge = {}
                for j in players_in_game:
                    child_knowledge[j] = set()
                    player_knowledge[i] = child_knowledge
    
    for k in player_knowledge:
        for l in player_knowledge:
            if k == l:
                player_knowledge[k][l] = set(hands[k]) 
    
    
    print(player_knowledge)
    #print(hands)
    starting_player_index = players_in_game.index(starting_player)

    #Then, given this initial information, we now make some turns
    for i in range(turns):
        #Who's turn is it (starting_player = current player)
        #print(starting_player_index)

        suggestion = {
                    "Suspect": random.choice(suspects),
                    "Weapon": random.choice(weapons),
                    "Room": random.choice(rooms)
                }
        suggestion_cards = list(suggestion.values()) 
    
        players_after_suggesting_player = players_in_game[starting_player_index + 1:]
        players_before_suggesting_player = players_in_game[:starting_player_index]

        players_outside_of_suggestion_player = (
            players_after_suggesting_player
            + players_before_suggesting_player
        )
        suggestion_output()
        starting_player_index += 1
        if starting_player_index % len(players_in_game) == 0:
             starting_player_index = 0
        for x in player_knowledge: #How to print multiple lines https://stackoverflow.com/questions/34980251/how-to-print-multiple-lines-of-text-with-python 
             print (f'{x} knowledge')
             for y in player_knowledge[x]:
                  print(y, ':', player_knowledge[x][y])
             print() #print empty line https://stackoverflow.com/questions/13872049/print-empty-line 
        i += 1

    

game_simulation(10)

    
#Checks:
#1. Every player exists in the knowledge structure. 
#Check

#2. The suggesting player's own hand is stored as known information.
#Check

#3. If someone shows a card, that card is stored under the correct player.
#Check

#4. If nobody disproves, no new HAVE knowledge is added.
#Check

#5. The same known card should not be stored twice.
#Check

#6. The knowledge structure must not reveal cards that were never shown.
#Check


#Additional questions:
#Why is a dictionary useful for storing player knowledge?
#You get a full overview of the knowledge in the game, which is different for each player.

#Why might a set be better than a list for confirmed cards?
#It prevents duplicates. 

#Topics covered in this piece of code:
#nested data structures, dictionaries, sets, storing game knowledge, updating state, avoiding duplicates, None checks


#AI:

#The use of player_knowledge[f'Player {starting_player_index+1}'][q] is nice now that I use 'Player 1', 'Player 2' etc., but does not work when I use real names. 
#Instead, I already had the current player with players_in_game[starting_player_index]. I will fix this in the next exercise.

#Using sets is more future proof (Already changed this in the code, as we will need this in the next exercise.)

#i += 1 is unnecessary