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


deck = generate_deck(1)
print(deck)
