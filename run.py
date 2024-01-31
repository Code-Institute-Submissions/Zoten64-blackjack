# Import statements
import random

# Variables

# code taken here:
# https://www.geeksforgeeks.org/how-to-print-a-deck-of-cards-in-python/
# a list of all the suits in unicode. Resulting characters: ♣ ♥ ♦ ♠
suits = ["\u2663", "\u2665",
         "\u2666", "\u2660"]
# a list of all the ranks
ranks = ['A', '2', '3', '4', '5',
         '6', '7', '8', '9', '10',
         'J', 'Q', 'K']
dealers_score = 0
players_score = 0
deck_count = 0

# Functions


def generate_deck(number_of_decks):
    """
    Generates a list of all the cards. Takes the argument 'number_of_decks'
    to determine the amount of decks to pick cards from.
    """
    # Code referenced from here:
    # https://www.geeksforgeeks.org/how-to-print-a-deck-of-cards-in-python/
    # Code has been changed slightly to fit this function
    # A temporary deck is created in order to not overwrite any
    # existing deck variable. This will be returned at the end of the function.
    temp_deck = []
    for i in range(number_of_decks):
        for suit in suits:
            for rank in ranks:
                temp_deck.append(rank + suit)
    return temp_deck


#Starter code

print("How many decks do you want to play with? If unsure enter 1")
#This will loop the code until the player enters a valid number
while True:
    try:
        deck_count = input()
        if int(deck_count) > 0:
            #if the number is valid it breaks out of the loop
            break
        else:
            print(f"You cannot play with {deck_count} decks. " 
                  "Enter a number above 0")
    except:
        #If there's an error, most likely because the player did not
        #Enter an integer, this will run
        print("Input has to be a whole number. Try again:")

#temporary testing code
deck = generate_deck(int(deck_count))
print(deck, len(deck))
    
