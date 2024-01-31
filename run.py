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


def deck_number():
    """
    Makes the user input a number of decks they want to play with
    """
    print("How many decks do you want to play with? If unsure enter 1")
    # This will loop the code until the player enters a valid number
    while True:
        try:
            deck_count = input()
            if int(deck_count) > 0:
                # if the number is valid it breaks out of the loop
                break
            else:
                print(f"You cannot play with {deck_count} decks. "
                      "Enter a number above 0")
        except:
            # If there's an error, most likely because the player did not
            # Enter an integer, this will run
            print("Input has to be a whole number. Try again:")

    # temporary testing code
    deck = generate_deck(int(deck_count))
    print(deck, len(deck))


def how_to_play():
    """
    Explains the basics of the game to the user
    """
    #Empty prints makes a space to make the output more readable
    print("How to play:")
    print()
    print("Your goal is to try and beat the dealer by having your total "
          "amount of cards value be closer to 21 than the dealer's cards")
    print()
    print("All face cards have a value of 10. Ace has a value of "
          "1 or 11 depending on if your hand exceeds 21. The rest have "
          "the same value as the number of the card\n")
    print()
    print("You will recieve 2 cards to start with. The dealer will have "
          "one card facing up and one card facing down. Based on this "
          "you can make a guess of how many points the dealer might have " 
          "to determine your next move \n"
          "You have the option to either hit or stand. If you hit "
          "you will be given another card. If you stand the dealer will "
          "reveal their hidden card. If the dealer's cards amount "
          "to less than 17 they have to hit. If their cards amount to "
          "17 or more they have to stand.\n")
    print()
    print("A bust is an automatic loss. This is when your total cards "
          "exceed the value of 21.\n"
          "If you bust you lose. If the dealer busts you win.")
    print()
    print("At the start of the game you'll place a bet. If you win you "
          "get double your bet back. \n"
          "If your two starting cards has a value of 21 you will immediately " 
          "get 1.5x your bet back. This is called a natural blackjack")
    


# Starter code
how_to_play()