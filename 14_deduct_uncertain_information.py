#Exercise 14: Deduce HAVE knowledge from uncertain groups
#Using the UNCERTAIN knowledge from exercise 13,
#the goal is now to make the first real deduction.


#14.1
#If information in have or not have information, remove it from the uncertain set.

#We can do that by inspecting one uncertain group, and then loop through the all player HAVE cards and then through the player NOT HAVE cards 

#14.2
#If one element is left in the uncertain set, and it is not part of another uncertin set, then the set is terminated and the element is added to HAVE_knowledge


#Next exercise we can further deduce so we can:
#Add handcard information


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

#In this exercise, the complexity went further up. It was though as the loops become increasingly nested and more difficult to read.
#I may introduce a function in exercise 15.
#Also, I observe that further deductions are possible via:
#If 3 people don't NOT HAVE a card, it must belong to the last person
#If we know handcards, we can also deduce cards this way.



def game_simulation(turns):

    def deduction_engine():
        knowledge_changed = True #From here, start the deduction engine.
        while knowledge_changed:
            knowledge_changed = False
            for observer in players_in_game:
                for target in players_in_game:
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
                                        knowledge_changed = True
                                        print(f'{observer} DEDUCTED {card} FOR {target}!') #For debugging reasons
                                resolved_groups.append(uncertain_group)
                            if len(remaining_cards) == 0:  #This would mean the stored knowledge is contradictory. The clause says the target has at least one of those cards, while NOT HAVE rules rules all of them out. 
                                print("Houston, we have a problem!")
                        for group in resolved_groups:
                            player_UNCERTAIN_knowledge[observer][target].remove(group)
                                    #THIS BECOMES A RECURSIVE LOOP! Here I asked AI what best to do, I suggested a recursive loop, but it responded with the idea of knowledge propagation.
                                    #This way, we check if knowledge_changed = True, then loop, until knowledge_changed = False.

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

    

game_simulation(6)



#Topics introduced:
#nested loops/lists, looping through lists/sets, knowledge_representation

#AI:
#Suggested to use knowledge representation rather than making a recursive loop, which I think is a good idea.
#I looped the uncertain sets first, and then the players/targets (q). But this led to weird results.
#I did not know how to get the deducted sets out of player_UNCERTAIN_knowledge. Once again, for sets, one should work outside the loop. So I gathered the sets that led to deductions in player_HAVE_knowledge, stored them in resolved_sets and deleted them afterwards.
#I made a function for the deduction engine, but put it in a loop, which led to running the deduction engine too often.
#In an edge case, it could be possible to add a uncertain_knowledge clause with one item to player_UNCERTAIN_knowledge, which led to a clause_solved knowledge representation