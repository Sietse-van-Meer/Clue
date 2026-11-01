#Exercise 17: Advanced hand-size deduction
#Combine UNCERTAIN clauses with the number of remaining free cards in a player's hand.

#Example:
#Player 3 has 4 cards total.
#3 cards are already known.
#
#UNCERTAIN:
#{"Plum", "dagger"}
#{"Plum", "library"}
#
#Only one hand slot remains.
#Both clauses must be true.
#Therefore the remaining card must be Plum.


#17.1 calculate how many unknown hand slots remain for each target
#17.2 Look at all unresolved uncertain clauses for that target toghether instead of treating every clause completely independently
#17.3 Find deductions that follow because only a limited of unknown hands can still fit in the target's hand
#17.4 Add newly certain cards to HAVE and propagate them normally


#From previous exercises
import random
from itertools import combinations

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
                all_seen_cards = set()
                
                for target in players_in_game:

                        #Deduct envelope candidates
                        all_seen_cards.update(player_HAVE_knowledge[observer][target]) 


                        #Deduct handcards
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


                        #Advanced hand card deduction using number of unknown cards in hand
                        player_UNKNOWN_hand_knowledge[observer][target] =  hand_TOTAL_knowledge[observer][target] - len(player_HAVE_knowledge[observer][target]) 
                        clauses = player_UNCERTAIN_knowledge[observer][target]
                        #Make the possible_clauses set with items to use for intersection with all combinations of possible cards.

                        #If there is a card that intersects with ALL combinations, the player must HAVE this card.
                        possible_clause_cards = set()
                        for clause in clauses:
                            possible_clause_cards.update(clause)
        
                        valid_combinations = []
        
                        for r in range(1, player_UNKNOWN_hand_knowledge[observer][target]+1):
                            card_combinations = combinations(possible_clause_cards,r) #from itertools
                            for combination in card_combinations:
                                combination_set = set(combination)
                                combination_valid = True
                                for clause in clauses:
                                    intersection = combination_set & clause 
                                    if len(intersection) == 0:
                                        combination_valid = False 
                                if combination_valid:
                                    valid_combinations.append(combination_set)
                        if valid_combinations:
                            definite_cards = set.intersection(*valid_combinations)
                            new_definite_cards = definite_cards - player_HAVE_knowledge[observer][target]
                            if new_definite_cards:
                                player_HAVE_knowledge[observer][target].update(new_definite_cards)
                                for player in players_in_game:
                                    if player != target:
                                        player_NOT_HAVE_knowledge[observer][player].update(new_definite_cards)
                                knowledge_changed = True

                envelope_deduction = False
                #Envelope deduction part 1: If nobody has a card, it must be part of the envelope!
                for card in total_cards:

                    nobody_has_card = True
                    for target in players_in_game:
                        if card not in player_NOT_HAVE_knowledge[observer][target]:
                            nobody_has_card = False

                    
                    if nobody_has_card: #If nobody has the card, it must be in the envelope
                        if card in suspects:
                            if card not in player_confirmed_envelope_cards[observer]["Suspect"]: #Avoid endless loops
                                player_confirmed_envelope_cards[observer]["Suspect"].add(card)
                                print(f'Suspect in envelope deduction for {observer}!')
                                envelope_deduction = True 
                        if card in weapons:
                            if card not in player_confirmed_envelope_cards[observer]["Weapon"]:
                                player_confirmed_envelope_cards[observer]["Weapon"].add(card)
                                print(f'Weapon in envelope deduction for {observer}!')
                                envelope_deduction = True 
                        if card in rooms:
                            if card not in player_confirmed_envelope_cards[observer]["Room"]:
                                player_confirmed_envelope_cards[observer]["Room"].add(card)
                                print(f'Room in envelope deduction for {observer}!')
                                envelope_deduction = True             

                #Envelope deduction part 2: If only one card is available in a category to be in the envelope, it must be part of the envelope!
                suspect_cards_seen = [x for x in all_seen_cards if x in suspects] #It was actually most difficult to find out at what indent to put this part of the code
                weapon_cards_seen = [x for x in all_seen_cards if x in weapons] #We gather cards in the inner loop and then summarize / categorize after the loop
                room_cards_seen = [x for x in all_seen_cards if x in rooms]

                if len(player_confirmed_envelope_cards[observer]["Suspect"]) == 1:
                    suspect_candidates = list(player_confirmed_envelope_cards[observer]["Suspect"]) #next(iter()) allows us to 1. iterate over the list, and next will just give us the first element.
                else: 
                    suspect_candidates = [x for x in suspects if x not in suspect_cards_seen]

                if len(player_confirmed_envelope_cards[observer]["Weapon"]) == 1:
                    weapon_candidates = list(player_confirmed_envelope_cards[observer]["Weapon"])
                else: 
                    weapon_candidates = [x for x in weapons if x not in weapon_cards_seen]

                if len(player_confirmed_envelope_cards[observer]["Room"]) == 1:
                    room_candidates = list(player_confirmed_envelope_cards[observer]["Room"])
                else:
                    room_candidates = [x for x in rooms if x not in room_cards_seen]


                
                player_envelope_candidates[observer]["Suspect"] = suspect_candidates
                player_envelope_candidates[observer]["Weapon"] = weapon_candidates
                player_envelope_candidates[observer]["Room"] = room_candidates

                if len(player_envelope_candidates[observer]["Suspect"]) == 1:
                    envelope_card = next(iter(player_envelope_candidates[observer]["Suspect"])) #Next(iter()) takes the first string from the envelope in the corresponding category (it can only be one card of course per category)
                    if envelope_card not in player_confirmed_envelope_cards[observer]["Suspect"]:
                        player_confirmed_envelope_cards[observer]["Suspect"].add(envelope_card)
                        envelope_deduction = True 
                if len(player_envelope_candidates[observer]["Weapon"]) == 1:
                    envelope_card = next(iter(player_envelope_candidates[observer]["Weapon"])) 
                    if envelope_card not in player_confirmed_envelope_cards[observer]["Weapon"]:
                        player_confirmed_envelope_cards[observer]["Weapon"].add(envelope_card)
                        envelope_deduction = True 
                if len(player_envelope_candidates[observer]["Room"]) == 1:
                    envelope_card = next(iter(player_envelope_candidates[observer]["Room"]))
                    if envelope_card not in player_confirmed_envelope_cards[observer]["Room"]:
                        player_confirmed_envelope_cards[observer]["Room"].add(envelope_card)
                        envelope_deduction = True 
                        #All other cards in this category are in someone's hands! 
                
                #Propagation to NOT_HAVE knowledge of other players
                if envelope_deduction == True:
                    # Propagate confirmed envelope knowledge
                    for category in categories:
                        for envelope_card in player_confirmed_envelope_cards[observer][category]: #For each card that we find in the envelope, we know the other players do not have this card in their hand.

                            for target in players_in_game:
                                if envelope_card not in player_NOT_HAVE_knowledge[observer][target]:
                                    player_NOT_HAVE_knowledge[observer][target].add(envelope_card)
                                    #Now loop to the start again
                                    knowledge_changed = True

                #Deduction 3: If card is not in the envelope and can only be in one player's hand, this player must have this card.
                for card in total_cards:
                    possible_players = []
                    for target in players_in_game:
                        if card not in player_NOT_HAVE_knowledge[observer][target]:
                            possible_players.append(target) #Somebody can still have the card

                    if len(possible_players) == 1: #If the card is NOT in the envelope and can only be in one player's hands, it is in that player hand.
                        possible_player = possible_players[0] #Index the only possible player
                        if card in suspects:
                            if card not in player_envelope_candidates[observer]["Suspect"]:
                                if card not in player_HAVE_knowledge[observer][possible_player]:
                                    player_HAVE_knowledge[observer][possible_player].add(card)
                                    for player in players_in_game:
                                        if player != possible_player:
                                            player_NOT_HAVE_knowledge[observer][player].add(card)
                                    knowledge_changed = True
                        if card in weapons:
                            if card not in player_envelope_candidates[observer]["Weapon"]:
                                if card not in player_HAVE_knowledge[observer][possible_player]:
                                    player_HAVE_knowledge[observer][possible_player].add(card)
                                    for player in players_in_game:
                                        if player != possible_player:
                                            player_NOT_HAVE_knowledge[observer][player].add(card)
                                    knowledge_changed = True
                        if card in rooms:
                            if card not in player_envelope_candidates[observer]["Room"]:
                                if card not in player_HAVE_knowledge[observer][possible_player]:
                                    player_HAVE_knowledge[observer][possible_player].add(card)
                                    for player in players_in_game:
                                        if player != possible_player:
                                            player_NOT_HAVE_knowledge[observer][player].add(card)
                                    knowledge_changed = True

                
        print(player_envelope_candidates)
        print(player_confirmed_envelope_cards)
        print(player_UNKNOWN_hand_knowledge)

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
    player_envelope_candidates = {}
    player_confirmed_envelope_cards = {}
    player_UNKNOWN_hand_knowledge = {}
   

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

    #New nested dictionary in which we can see what envelope cards each player knows
    categories = ["Suspect", "Weapon", "Room"]
    for i in players_in_game:
        player_envelope_candidates[i] = {}
        for j in categories:
            player_envelope_candidates[i][j] = []

    for i in players_in_game:
        player_confirmed_envelope_cards[i] = {}
        for j in categories:
            player_confirmed_envelope_cards[i][j] = set()
    

    #How to get the length of the list within the dictionary
    for i in hands:    
            child_TOTAL_hand_knowledge = {}
            for j in hands:
                child_TOTAL_hand_knowledge[j] = len(hands[j])
                hand_TOTAL_knowledge[i] = child_TOTAL_hand_knowledge

    for i in players_in_game:
            child_UNKOWN_hand_knowledge = {} #NOT_HAVE_knowledge
            for j in players_in_game:
                 child_UNKOWN_hand_knowledge[j] = 0 #amount of unknown cards is not a set or a list of course. It is just an integer, so initializing with 0 is fine.a
                 player_UNKNOWN_hand_knowledge[i] = child_UNKOWN_hand_knowledge
                
    print(player_UNKNOWN_hand_knowledge)
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

    

game_simulation(1)



#Topics introduced:
#Combinations using combinations() from itertools, intersection between multiple sets


#AI: 
#While in contrast with the idea of this project, I bumped my head so often on this exercise, I did need help from AI.
#The logic was simple to think out, but the implementation was tedious.
#First, it is important to note this is a niche case, yet an important one.
#Using the number of unknown cards remaining in a player's hand, we generate possible combinations of cards from the unresolved UNCERTAIN clauses.
#We then keep only the combinations that satisfy every clause. If a card occurs in every valid combination, that player must HAVE that card.
#For example, if a player has only one unknown card left and the unresolved clauses are: {plum, dagger} and {plum, library}, you can deduce plum must be the last card in this player hand, since it appears as the only card that can satisfy both clauses.
