#We start making Clue from zero.
#We code without AI, to learn python. AI is used to judge my code in the end. 

#Exercise 1: make the representitive cards in Clue
#1.1 Make each category a python list
#1.2 Make one big card list
#Print the amount of suspects, weapons, rooms, and total number of cards

#Clue has 3 categories
#6 suspects: Green, Mustard, Peacock, Plum, Scarlett, White
#6 weapons: candlestick, dagger, lead piping, revolver, rope, spanner
#9 rooms: ballroom, billiard room, conservatory, dining room, hall, kitchen, library, lounge, study

suspects = ["Green", "Mustard", "Peacock", "Plum", "Scarlett", "White"]
weapons = ["candlestick", "dagger", "lead piping", "revolver", "rope", "spanner"]
rooms = ["ballroom", "billiard room", "conservatory", "dining room", "hall", "kitchen", "library", "lounge", "study"]

#Idea 1: Merge lists using pandas pd.merge -> doesnt work like that, it is used for datafranes
#Idea 2: a + b + c, from https://www.geeksforgeeks.org/python/python-ways-to-concatenate-two-lists/
total_cards = suspects + weapons + rooms

#Print length, using len()
print(f"Number of suspects: {len(suspects)}") 
print(f"Number of weapons: {len(weapons)}") 
print(f"Number of rooms: {len(rooms)}")
print(f"Total number of cards: {len(total_cards)}")


#Now it worked
#Covered in this piece of code: lists, merging lists, f strings.

#AI review: pass, but leave out libraries if you don't use them. 8.5/10