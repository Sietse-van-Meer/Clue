#Exercise 15: Deduce using player hand sizes
#Use the fixed number of cards in each player's hand as a new deduction rule.

#15.1 Store each player's hand size dynamically.
#Example:
#hand_sizes = {
#    "Player 1": 5,
#    "Player 2": 5,
#    "Player 3": 4
#}

#15.2 In deduction_engine(), add cards to known hand cards if they are in HAVE_knowledge.
#compare: len(player_HAVE_knowledge[observer][target]) with: hand_sizes[target]

#15.3 If the known HAVE cards equal the target's hand size,
#the observer knows that every other card is NOT HAVE.
#Only set knowledge_changed = True when new information is actually added.

#15.4 Add a contradiction check:
#if known HAVE cards > hand size:
#    print a warning



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





def game_simulation(turns):

    def deduction_engine():
        knowledge_changed = True #From here, start the deduction engine.
        while knowledge_changed:
            knowledge_changed = False
            for observer in players_in_game:
                for target in players_in_game:
                        if len(player_HAVE_knowledge[observer][target]) == hand_TOTAL_knowledge[observer][target]: #I should not forget the [observer][target], and I had to put it high in the deduction chain. (not below in uncertain groups etc.)
                            rest_cards = [x for x in total_cards if x not in player_HAVE_knowledge[observer][target]] #I knew I had to set knowledge_changed, to True here, but did not know how! Just check before and after and it is simple!
                            before = len(player_NOT_HAVE_knowledge[observer][target])
                            player_NOT_HAVE_knowledge[observer][target].update(rest_cards)
                            after = len(player_NOT_HAVE_knowledge[observer][target])
                            if after > before:
                                knowledge_changed = True
                        if len(player_HAVE_knowledge[observer][target]) > hand_TOTAL_knowledge[observer][target]:
                            print("Houston, we have a hand problem!")
                        resolved_groups = [] #Empty list which we fill with sets that should be removed from player_UNCERTAIN_knowledge
                        for uncertain_group in player_UNCERTAIN_knowledge[observer][target]: #Layer 1 prints [{set 1}, {set 2}]
                            clause_solved = False #But we also must check if the clause consists of a card that is already in have. Then, we want to remove this clause (we already know one of the cards)
                            remaining_cards = set()
                            
                            for card in uncertain_group: #Check every card in every group
                                if card in player_HAVE_knowledge[observer][target]:
                                    clause_solved =True
                                if card not in player_NOT_HAVE_knowledge[observer][target]: #Check then for each player, do they HAVE or NOT_HAVE this card? Because of the link from HAVE TO NOT_HAVE, checking NOT_HAVE is enough.
                                    remaining_cards.add(card) #You get a nasty error that you cannot remove items from a set while looping over that same set... 
                                    #One has to work with either a copy or a new reduced set. But then, you only want to change one uncertainty set a time, to still work with clauses.
                            if clause_solved:
                                resolved_groups.append(uncertain_group)
                                continue #skips the rest of the loop iteration so we go to the next clause. Later this clause will be removed from player_UNCERTAIN_knowledge
                            if len(remaining_cards) > 1:
                                uncertain_group.clear() 
                                uncertain_group.update(remaining_cards)    
                            if len(remaining_cards) == 1:
                                for card in remaining_cards:
                                    if card not in player_HAVE_knowledge[observer][target]:
                                        player_HAVE_knowledge[observer][target].add(card)
                                        for player in players_in_game: 
                                            if player != target:
                                                player_NOT_HAVE_knowledge[observer][player].add(card) #If disprover show the suggesting player a card, it is not in other player's hands.                                        
                                        knowledge_changed = True
                                        print(f'{observer} DEDUCTED {card} FOR {target}!') #For debugging reasons
                                        
                                resolved_groups.append(uncertain_group)
                            if len(remaining_cards) == 0:  #This would mean the stored knowledge is contradictory. The clause says the target has at least one of those cards, while NOT HAVE rules rules all of them out. 
                                print("Houston, we have a problem!")
                        for group in resolved_groups:
                            player_UNCERTAIN_knowledge[observer][target].remove(group)

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
                                player_UNCERTAIN_knowledge[player][q].append(set(suggestion_cards))   #Append a new set 
                    deduction_engine()
                                    
                    return disproving_player, shown_card
                else:
                    disproving_player = q
                    for player in players_in_game:
                            player_NOT_HAVE_knowledge[player][disproving_player].update(suggestion_cards) #If one cannot disprove, it has none of the suggestion cards
                    deduction_engine()
                    print(f'{q} cannot disprove')

        print("Nobody could disprove this suggestion")
        return None, None #Return nothing

    #Initial knowledge 
    players_in_game = list(hands.keys())

    #Randomly choose the first player
    starting_player = random.choice(list(hands.keys()))

    player_HAVE_knowledge = {}
    player_NOT_HAVE_knowledge = {}
    player_UNCERTAIN_knowledge = {}
    hand_TOTAL_knowledge = {}

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
    
    #print(f'Player HAVE knowledge{player_HAVE_knowledge}')
    #print(f'Player NOT HAVE knowledge {player_NOT_HAVE_knowledge}')
    #print(f'Player UNCERTAIN knowledge {player_UNCERTAIN_knowledge}')    

    #How to get the length of the list within the dictionary
    for i in hands:    
            child_TOTAL_hand_knowledge = {}
            for j in hands:
                child_TOTAL_hand_knowledge[j] = len(hands[j])
                hand_TOTAL_knowledge[i] = child_TOTAL_hand_knowledge
                
    #hand_TOTAL_knowledge = {player: len(items) for player, items in hands.items()}
    print(hand_TOTAL_knowledge)

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
                        print(y, ': HAVE :', player_HAVE_knowledge[x][y], '; NOT HAVE :', player_NOT_HAVE_knowledge[x][y], '; UNCERTAIN :', player_UNCERTAIN_knowledge[x][y], 'Knows ', len(player_HAVE_knowledge[x][y]), 'from the total', hand_TOTAL_knowledge[x][y], 'cards')
             print() #print empty line https://stackoverflow.com/questions/13872049/print-empty-line

    

game_simulation(38)



#Topics introduced:
#nested loops/lists, looping through lists/sets, knowledge_representation, knowledge propagation, combining deduction rules

#AI:
#I first tried to have KNOWN and TOTAL player hand count. In the end, I changed the KNOWN to len(player_HAVE_knowledge), which is a much simpler and more consistent solution.
#I also first tried to put the hand deduction loop too deep in the deduction engine, making it only trigger on rare instances
#After a week of not doing the project, I sometimes still make mistakes trying to select objects in the nested dictionary (using hand_TOTAL_knowledge, rather than hand_TOTAL_knowledge[observer][target])
#Using a simple before/after comparison, I could easily implement the knowledge_changed to True clause. I hesitated to implement this to prevent neverending loops.