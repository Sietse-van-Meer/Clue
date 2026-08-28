#Exercise 5: Deal the cards to players

#We start with a fixed number of players
players = ["Player 1", "Player 2", "Player 3"]


#Deal all the cards from the shuffled deck one by one in turn.


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

#Deal to players
#Hint, use modulo operator, %
#Idea 1: Make for each player a list. Add to each list using a for loop.

#5.1 Why uses lists? 
#Well, dictionary uses {key, value}, and it does not seem efficient to use {player, cards}.
#A tuple is not mutable so not useful, a set could be another option. But let's keep the order (possibly for future indexing), so we use lists.

#5.2 How do you assign cards to players one after another

#Let's initialize the lists
player_1_hand = []
player_2_hand = []
player_3_hand = []

#Testing out the modulo operator
#print(0%3) -> 0
#print(1%3) -> 1
#print(2%3) -> 2
#print(3%3) -> 0

#We can use enumerate to split index and item! https://stackoverflow.com/questions/522563/how-can-i-access-the-index-value-in-a-for-loop
#for index, item in enumerate(shuffled_deck):
#   print(index, item) 

#Now we can make a loop: https://www.w3schools.com/python/python_lists_loop.asp
#Add item i to the list. Use [i], list(i) only gives the first letter.
for index, i in enumerate(shuffled_deck):
    if index % 3 == 0:
        player_1_hand += [i]
    elif index % 3 == 1:
        player_2_hand += [i]
    elif index % 3 == 2:
            player_3_hand += [i]
    else:
         print("Error, possibly you play with another player amount than 3.")

#Check hand cards
print(f'player 1 hand: {player_1_hand}')
print(f'player 2 hand: {player_2_hand}')
print(f'player 3 hand: {player_3_hand}')

#Check length
print(f'Length player 1 hand: {len(player_1_hand)}')
print(f'Length player 2 hand: {len(player_2_hand)}')
print(f'Length player 3 hand: {len(player_3_hand)}')

#5.3 How can you make the player order repeat after player 3?
#Well, using the modulo operator, you tell the code who to deal. When the index goes to a number that /3 has no remainders, we
#know it is player 1's turn again, looping the order again.

#5.4 What does the % (modulo) operator do in Python
#It returns the remainder after a division. Like 5%2 returns 1, as 5 cannot be divided exactly by 2.

#5.5 Can you solve the dealing without using modulo?
#Possibly we can use a list of lists, using player_1_hand, player_2_hand, and player_3_hand as items in the new list.
#order_list = [player_1_hand, player_2_hand, player_3_hand]
#print(order_list)
#Seems to work
#Let's initialize the lists again
player_1_hand = []
player_2_hand = []
player_3_hand = []

print(f'player 1 hand: {player_1_hand}')
print(f'player 2 hand: {player_2_hand}')
print(f'player 3 hand: {player_3_hand}')

order_list = [player_1_hand, player_2_hand, player_3_hand]
#I asked AI for a hint, since I still did not figure out how to loop.
#It said I could look at while loops, and that logic fits I think.

i = 0
while i < len(deck): #Not <=, else you will go out of bounds
     for index, item in enumerate(order_list): 
          item.append(shuffled_deck[i])  #You can use append to specifically add the item from deck. 
          i += 1

print(f'player 1 hand: {player_1_hand}')
print(f'player 2 hand: {player_2_hand}')
print(f'player 3 hand: {player_3_hand}')

print(f'Length player 1 hand: {len(player_1_hand)}')
print(f'Length player 2 hand: {len(player_2_hand)}')
print(f'Length player 3 hand: {len(player_3_hand)}')


#And that works. That was the first time, I actually struggled with the solution. 
#I had to use a combination of a while and for loop, that was a little tricky.
#First, I initialize i as 0.
#Second, I make integer 'i' go from 0 until the length of the deck (< len(deck) because we count from 0).
#But it only updates at the end of a for loop. As long as i < len(deck) we activate a for loop, which appends 
#one item to every list entry. Then, after it is done, it exits the for loop, check the while loop condition, 
#and if still true, it will add again items until deck is empty. This is a decent solution, but a more difficult exercise.

#Topics covered in this piece of code: modulo operator (%), if/elif/else statements, while loops, for loops, nested loops, enumerate.

#AI: 
#1. Helped with a hint to use a while loop, also helped me understand that 'for index, item in enumerate(order_list):' goes 
#automatically over all three elements in the order_list.

#2. The second solution can cause an IndexError if the number of cards dealt is not divisible by the number of players. 
#3. Finally, it disagrees that dictionaries are not efficient in this situation. So you could get
#   hands = {"Player 1": [revolver, Mustard, rope], "Player 2": [conservatory, dining room, Plum], "Player 3": [study, kitchen, ballroom]}

#So this exercise was not as succesful, still we got some good ideas, and I will continue using the dealing method using the 
#modulo operator and using dictionary to combine information about the players and their handcards.