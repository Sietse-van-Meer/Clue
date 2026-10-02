#Exercise 13: Store uncertain knowledge from a hidden disproving card


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





#Exercise 13:
#We now want three different kinds of knowledge.

#13.1 Create an UNCERTAIN knowledge structure
#1. HAVE knowledge:
#Cards we know a player definitely owns.

#2. NOT HAVE knowledge:
#Cards we know a player definitely does not own.

#3. UNCERTAIN / ONE-OF
#Player owns at least one card from a group,
#but we do not yet know which one.

#Maybe a list with multiple sets (multiple one of constraints)
#Player 1": {"Player 1": NOT RELEVANT,
#            "Player 2": [(SET 1), (SET 2)],
#            "Player 3": [(SET 1), (SET 2)],
#            "Player 4": [(SET 1), (SET 2)]}


#13.2 Store uncertain knowledge when someone disproves
#13.3 Avoid storing the same uncertain group twice

#I found this problem particularly difficult and had to resort to AI since I was not able to fix the list/set issue. In the end, the fix was actually not that big.
#The outer layer is a dictionary, with lists containing uncertain sets. This because you want to add multiple uncertain lists. However, you have to control for doubles in the if statement. 
#You append to the list using .append, and the individual set should not be equal to another set (remember sets have no order, so (Green, dagger, kitchen) == (dagger, Green, kitchen)).
#We reduce/trim the sets logically further in exercise 14.



def game_simulation(turns):

    def suggestion_output():
        print(f'Player {starting_player_index+1} turn.  Player {players_in_game[starting_player_index]} suggests: {suggestion_cards}')
        for q in players_outside_of_suggestion_player: 
                print(f'Checking {q}')
                matches = [x for x in hands[q] if x in suggestion_cards]
                
                if matches:
                    disproving_player = q
                    shown_card = random.choice(matches)
                    current_player = players_in_game[starting_player_index]
                    print(f'{disproving_player} shows player {starting_player_index + 1}: {shown_card}')
                    player_HAVE_knowledge[players_in_game[starting_player_index]][q].add(shown_card)  #Link starting_player_index to keys in player_HAVE_knowledge, and sets can't have duplicates.
                    for player in players_in_game:
                        if player != q:
                              player_NOT_HAVE_knowledge[players_in_game[starting_player_index]][player].add(shown_card) #If disprover show the suggesting player a card, it is not in other player's hands.
                              if player !=q and player != current_player and set(suggestion_cards) not in player_UNCERTAIN_knowledge[player][q]: #You need set, else you compare a list with a set
                                player_UNCERTAIN_knowledge[player][q].append(set(suggestion_cards))   #This is not perfect yet, but a good start for exercise 13.
                    return disproving_player, shown_card
                else:
                    disproving_player = q
                    for player in players_in_game:
                            player_NOT_HAVE_knowledge[player][disproving_player].update(suggestion_cards)
                    print(f'{q} cannot disprove')

        print("Nobody could disprove this suggestion")
        return None, None #Return nothing

    #Initial knowledge is player_HAVE_knowledge
    #Make correct checking order

    #Initial knowledge 
    players_in_game = list(hands.keys())

    #Randomly choose the first player
    starting_player = random.choice(list(hands.keys()))

    player_HAVE_knowledge = {}
    player_NOT_HAVE_knowledge = {}
    player_UNCERTAIN_knowledge = {}


    for i in players_in_game:    
        child_HAVE_knowledge = {} #HAVE_knowledge
        for j in players_in_game:
            child_HAVE_knowledge[j] = set()
            player_HAVE_knowledge[i] = child_HAVE_knowledge

    for i in players_in_game:
        child_NOT_HAVE_knowledge = {} #NOT_HAVE_knowledge
        for j in players_in_game:
             child_NOT_HAVE_knowledge[j] = set()
             player_NOT_HAVE_knowledge[i] = child_NOT_HAVE_knowledge

    #I ran into typeError: list indices must be integers or slices, not str. List only accepts 0,1,2,3,...
    for i in players_in_game:
        child_UNCERTAIN_knowledge = {} #UNCERTAIN_HAVE_knowledge
        for j in players_in_game:
            child_UNCERTAIN_knowledge[j] = [] #So outer structure remains a dictionary, then the inner child is a list, and in the list we have sets
            player_UNCERTAIN_knowledge[i] = child_UNCERTAIN_knowledge

    for k in player_HAVE_knowledge: #Fill in handcard information
        for l in player_HAVE_knowledge:
            if k == l:
                player_HAVE_knowledge[k][l] = set(hands[k]) 

    for k in player_NOT_HAVE_knowledge: #Fill in handcard information
        for l in player_NOT_HAVE_knowledge:
            if k != l:
                player_NOT_HAVE_knowledge[k][l] = set(hands[k])
    
    
    print(f'Player HAVE knowledge{player_HAVE_knowledge}')
    print(f'Player NOT HAVE knowledge {player_NOT_HAVE_knowledge}')
    print(f'Player UNCERTAIN knowledge {player_UNCERTAIN_knowledge}')    
    #print(hands)
    starting_player_index = players_in_game.index(starting_player)

    #let's play some turns
    for i in range(turns):

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
        for x in player_HAVE_knowledge: #How to print multiple lines https://stackoverflow.com/questions/34980251/how-to-print-multiple-lines-of-text-with-python 
             print (f'{x} knowledge')
             for y in player_HAVE_knowledge[x]:
                    if x == y:
                        print(y, ': HAVE :', player_HAVE_knowledge[x][y], '; NOT HAVE : not relevant (all cards except hand cards) ; UNCERTAIN : not relevant')
                    elif x!=y:
                        print(y, ': HAVE :', player_HAVE_knowledge[x][y], '; NOT HAVE :', player_NOT_HAVE_knowledge[x][y], '; UNCERTAIN :', player_UNCERTAIN_knowledge[x][y])
             print() #print empty line https://stackoverflow.com/questions/13872049/print-empty-line

    

game_simulation(2)


#Topics covered in this piece of code:
#nested dictionaries, lists of sets

#AI:
#Helped me understand and fix errors caused by mixing up lists and sets,
#especially when storing uncertain knowledge as a list of sets.