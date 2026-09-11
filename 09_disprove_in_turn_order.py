#Exercise 9: Disprove suggestion in turn order
#Using the suggestion from exercise 7 and the checking logic from exercise 8,
#the goal is now to check players in the correct turn order. 
#In real Clue, only the first player after the suggesting player who can disprove gets to show a card.


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


#Shuffled deck
shuffled_deck = random.sample(deck, len(deck))


#Random number of players between 3 and 6
number_of_players = random.randint(3,6)


#Make player hands
hands = {}
i = 0
while i < number_of_players:
    hands.update({f'Player {i+1}':[]})
    i += 1


#Deal the cards
i = 0
while i < len(shuffled_deck):
    for key,value in hands.items():
        if i < len(shuffled_deck):
            value.append(shuffled_deck[i])
            i += 1


#Make suggestion
suggestion_player = random.choice(list(hands.keys()))
suggestion = {"Suspect": random.choice(suspects),"Weapon": random.choice(weapons),"Room": random.choice(rooms)
}

suggestion_cards = list(suggestion.values())
players_in_game = list(hands.keys())

#print(f'{suggestion_player} suggests: {suggestion_cards}')

def check_hands():
    disprove_cards = {}
    print(f'DEBUGGING: {suggestion_player} suggests: {suggestion_cards}')
    for player in players_in_game:
        if player != suggestion_player:
            matches = [x for x in hands[player] if x in suggestion_cards] #list(hands[player]) = hands[player] when using in!
            if matches:
                disprove_cards[player] = matches

    for player in hands.keys():
        if player != suggestion_player:
            if player in disprove_cards:
                print(f'DEBUGGING: {player} can disprove with {disprove_cards[player]}')
            else:
                print(f'DEBUGGING: {player} cannot disprove')

check_hands()

#9.1 Find the index of the suggestion player
#Using index, we can find a specific object in a list
suggestion_player_index = players_in_game.index(suggestion_player)
#print(suggestion_player_index)
#When for example player 4 suggests, the index is 3. This is correct, as Python starts indexes from 0.

#9.2 Find the next player
#This looks a bit like the modulo question we had before when dividing cards to players.
#When player 3 suggests and we play with 4 players.
#You first want player 4, then 1, then 2, then stop.
#We may want to use the modulo operator again (%)
#print(f'suggestion player index: {suggestion_player_index}')
#print(f'players in game: {len(players_in_game)}')

#debugging functions
#disprove_in_order()
#print(f'length players in game: {len(players_in_game)}')
#print(f'length players in game + 1: {len(players_in_game)}')
#print(f'length players in game + 1: {len(players_in_game) % len(players_in_game)}')

#https://www.reddit.com/r/learnpython/comments/vhbo0b/can_a_for_loop_start_somewhere_other_than_0/

#for j in players_in_game[suggestion_player_index + 1:]:
#        print(players_in_game.index(j))
#        #print(f'modulo: {(players_in_game.index(j) + 1) % len(players_in_game)}')
#        if (players_in_game.index(j) + 1) % len(players_in_game) == 0:
#            #print("I loop!")
#            for k in players_in_game:
#                if players_in_game.index(k) < suggestion_player_index:
#                    print(players_in_game.index(k))


#9.3 Check players in turn order
#We now want to check the other players one by one.

#For every player:
#1. Look at their hand
#2. Compare their cards with suggestion_cards
#3. If there are no matches, continue to the next player
#4. If there are matches, that player can disprove

#Empty list to compare to
# empty_list = []

# if suggestion_player_index + 1 == len(players_in_game):
#     for n in players_in_game:
#             if players_in_game.index(n) < suggestion_player_index:
#                                     matches = [x for x in hands[n] if x in suggestion_cards]
#                                     if matches == empty_list:
#                                         print(f'{n} no match')
#                                     elif matches != empty_list:
#                                         print(f'{n} shows {matches}')
#                                         break
#     if matches == empty_list: 
#                     print("Nobody could disprove this suggestion")
# else:
#     for j in players_in_game[suggestion_player_index + 1:]:
#             if (players_in_game.index(j) + 1) % len(players_in_game) != 0:
#                 matches = [x for x in hands[j] if x in suggestion_cards]
#                 if matches == empty_list:
#                     print(f'{j} no match')
#                 elif matches != empty_list:
#                     print(f'{j} shows {matches}')
#                     break
#             #print(f'modulo: {(players_in_game.index(j) + 1) % len(players_in_game)}')
#             elif (players_in_game.index(j) + 1) % len(players_in_game) == 0:
#                 matches = [x for x in hands[j] if x in suggestion_cards]
#                 if matches == empty_list:
#                     print(f'{j} no match')
#                     #print("I loop!")
#                     for k in players_in_game:
#                         if players_in_game.index(k) < suggestion_player_index:
#                             matches = [x for x in hands[k] if x in suggestion_cards]
#                             if matches == empty_list:
#                                 print(f'{k} no match')
#                             elif matches != empty_list:
#                                 print(f'{k} shows {matches}')
#                                 break
#                 elif matches != empty_list:  #Check for last player in the loop befor e looping back
#                     print(f'{j} shows {matches}')
#                     break
#                 if matches == empty_list: 
#                     print("Nobody could disprove this suggestion")


#Checks:

#1. The suggestion player is never checked.
#We always carefully choose avoid the suggestion player from being checked.

#2. The player directly after the suggestion player is checked first.
#We loop in order as established in 9.1, with extra logic to ensure:
    #If last player is suggestion player we simply iterate over the list up to the player who makes the suggestion.
    #If we loop up to the last player, we first inspect the matches of the last player and only reloop if no matches are found.

#3. If the last player makes the suggestion, Player 1 is checked first.
#The first if statement denotes the logic if the last player is the suggested player
#Then, one want to simply iterate over the list up to the player who makes the suggestion.

#4. Players without matching cards are skipped.
#Indeed, using if/else statements, players without matching cards are skipped.

#5. The first player with matching cards stops the search.
#Using if/else statements in combination with break, we can stop the loop if we found a matching hand.
#We could add in the future that only one of the cards is shown. For now, we show both.

#6. The code also works when nobody can disprove.
#Yes, if the final if statement is reached, that means no matches are found and then nobody could disprove the suggestion.


#Additional questions:
#How do you find the index of the suggestion player?
#One can find the index of a suggesting player (suggestion_player) in a list of players (players_in_game) using 
#list.index(suggestion_player). This way we make suggestion_player_index.

#How do you calculate the index of the next player?
#We use a for loop to loop over j items in players_in_game. 
#To reset the index, we use a modulo operator. This is handy, as dividing by the length of players_in_game, we can 
#tell the code that we ended up at the final player, hence continue the loop from the start of the list.

#Why do we stop checking after the first player can disprove?
#Because that is inherent to the Clue game.


#AI:
#I forgot one edge case, and did make the 'nobody can disprove' statement if the suggester was
#the last player in the list.

#Further, it finds that it is quite a complicated loop. 
#It wants me to use players_in_game[suggestion_player_index + 1:] for next players
#and players_in_game[:suggestion_player_index] for players before the suggestion player.
#It suggests to use one for loop.

#Better version with these limited clues:
players_after_suggesting_player_loop = players_in_game[suggestion_player_index + 1:]
players_before_suggesting_player_loop =  players_in_game[:suggestion_player_index]
empty_list = []

# if players_after_suggesting_player_loop == []:
#         for o in players_before_suggesting_player_loop:
#                 matches = [x for x in hands[o] if x in suggestion_cards]
#                 if matches == empty_list:
#                     print(f'NEW {o} no match')
#                 elif matches != empty_list:
#                     print(f'NEW {o} shows {matches}')
#                     break
#         if matches == empty_list:
#             print("NEW Nobody could disprove this suggestion")
# else:
#     for j in players_after_suggesting_player_loop: 
#         matches = [x for x in hands[j] if x in suggestion_cards]
        
#         if matches != empty_list:
#             print(f'NEW {j} shows {matches}')
#             break
#         elif matches == empty_list:
#             print(f'NEW {j} no match')
#             if (players_after_suggesting_player_loop.index(j) + 1) % len(players_after_suggesting_player_loop) == 0:
#                 #print("I loop!")
#                 for k in players_before_suggesting_player_loop:
#                     matches = [x for x in hands[k] if x in suggestion_cards]
#                     if matches != empty_list:
#                         print(f'NEW {k} shows {matches}')
#                         break
#                     if matches == empty_list:
#                         print(f'NEW {k} no match')

#                 if matches == empty_list:
#                     print("NEW Nobody could disprove this suggestion")

#One more hint, combine the lists!
players_outside_of_suggestion_player = players_after_suggesting_player_loop + players_before_suggesting_player_loop
empty_list = []

for q in players_outside_of_suggestion_player: 
        matches = [x for x in hands[q] if x in suggestion_cards]
        
        if matches != empty_list:
            print(f'FINAL {q} shows {matches}')
            break
        elif matches == empty_list:
            print(f'FINAL {q} no match')

if matches == empty_list:
    print("FINAL Nobody could disprove this suggestion")


#Topics covered in this piece of code:
#.index(), loops, list comprehension, if/elif statements, break
