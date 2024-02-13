# Import statements
import random
import os
import bcrypt
import pwinput
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Global variables

# code taken here:
# https://www.geeksforgeeks.org/how-to-print-a-deck-of-cards-in-python/
# a list of all the suits in unicode. Resulting characters: ♣ ♥ ♦ ♠
suits = ["\u2663", "\u2665",
         "\u2666", "\u2660"]
# a list of all the ranks
ranks = ['A', '2', '3', '4', '5',
         '6', '7', '8', '9', '10',
         'J', 'Q', 'K']
# A dictonary determining the value of each card rank.
card_value = {
    "A": 11,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10
}
highest_value = 21
dealers_score = 0
players_score = 0
balance = 1000
deck_count = 1
deck = []
username = ""


# Objects/classes


class account:
    '''Account related functions'''
    def try_again(prompt):
        '''
        The user will be asked if they want to try again
        The prompt variable will be printed making this code reuseable
        '''

        # The answer is immediately converted into lowercase to ensure
        # Case insensitivity
        ans = input(prompt).lower()
        if (ans == "y"):
            return True
        elif (ans == "n"):
            return False
        else:
            print("Invalid option.")

    def create_account():
        '''
        Create an account and put it into the database
        Returns "Unsuccessful" if the user cancels
        '''
        # Username or Password will equal "interrupted" if the user cancels
        # during one of the other called functions
        # If either of the functions called inside here returns "interrupted"
        # the function will return "unsuccessful"
        # Otherwise it returns the username
        username = account.create_username()
        if (username == "interrupted"):
            return "unsuccessful"

        password = account.create_password()
        if (password == "interrupted"):
            return "unsuccessful"
        else:
            # The data is made into a dictionary and put into the db
            data = {"username": username,
                    "password": password,
                    "balance": balance}
            db["player"].insert_one(data)
            return username

    def create_username():
        '''
        Lets user create a username
        Returns "interrupted" if the user cancels
        '''
        # Repeats until an available username is found or the user cancels
        # If an available username is found it returns it
        # If the user cancels the function will return "interrupted"
        while True:
            username = input("username: ")
            if account.username_exists(username):
                if (account.try_again("Username is taken. Try again? Y/N: ")
                        is False):
                    return "interrupted"
            else:
                return username

    def create_password():
        '''
        Lets user create a password.
        Returns "interrupted" if the user cancels.
        '''
        # This will loop until the passwords matches or the user cancels
        # Pwinput is used here to make the password hidden when the
        # user is typing it
        while True:
            password = pwinput.pwinput(prompt="Password: ", mask="*")
            password_confirm = pwinput.pwinput(prompt="Confirm password: ",
                                               mask="*")

            # If the passwords match the hash function will be called
            # and the result will be returned.
            # Otherwise it will ask the user if they want to try again
            if (password == password_confirm):
                return account.hash_password(password)
            else:
                if (account.try_again("Passwords do not match. "
                                      "Try again? Y/N: ") is False):
                    return "interrupted"

    # Both hash and check password functions reference this tutorial:
    # https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt/

    def hash_password(password):
        '''Hashes the password, aka encrypts it'''
        # Converts the password to bytes
        bytes = password.encode("utf-8")
        # Generates salt for a more secure encryption
        salt = bcrypt.gensalt()
        # Finally hashes the password
        hash = bcrypt.hashpw(bytes, salt)
        return hash

    def username_exists(username):
        '''
        Checks if a username exists.
        Returns True if the username exists.
        '''
        # Counts the amount of documents containing the username.
        # If the amount is not 0 the username is taken
        # Returns False if the username does not exist, and True if it does.
        if (db["player"].count_documents({"username": username})) == 0:
            return False
        else:
            return True

    def check_password(password, username):
        '''
        Checks if the password used to log in is correct.
        Returns True if the password is correct
        '''
        # Converts the password into bytes
        bytes = password.encode("utf-8")
        hash = db["player"].find_one({"username": username},
                                     {"password": True})["password"]

        # Checks if the password matches with that in the database
        # and returns the result.
        # Returns True if it's correct, False is it isn't
        return bcrypt.checkpw(bytes, hash)

    def log_in():
        '''
        Prompts the user for login information
        Returns "Unsuccessful" if the user cancels
        '''
        # The loop will make sure that the player enters a valid answer
        # In this case if the input is valid it enters the next loop
        # If the input is not valid it asks the user if they want to
        # Try again. If not it will break out of the loop, cancelling the
        # Whole operation.
        # If the user tries again it will loop back to the start
        while True:
            username = input("Username: ")
            # Check if there is a user with that name
            if account.username_exists(username) is False:
                # If the username is invalid the user will be prompted
                # to try again or cancel
                if (account.try_again("invalid username. Try again? Y/N: ")
                        is False):
                    # if the user doesn't want to try again the loop
                    # is broken out of
                    break
                else:
                    # Makes it loop back to the start
                    continue
            # Same loop concept as above, just with the password instead
            while True:
                password = pwinput.pwinput(prompt="Password: ", mask="*")
                account.check_password(password, username)
                if (account.check_password(password, username)):
                    print(f"Welcome {username}.")
                    break
                else:
                    if (account.try_again("invalid password. Try again? Y/N: ")
                            is False):
                        # if the user doesn't want to try again the loop
                        # is broken out of
                        break
                    else:
                        # Makes it loop back to the start
                        continue
            # If everything goes through the saved game is retrieved
            # From the database. Lastly the function returns the username
            game.get_saved_game(username)
            return username
        # If the user cancels the function returns "unsuccessful"
        return "unsuccessful"


class game:
    '''Game related functions'''
    def generate_deck(number_of_decks):
        """
        Generates a list of all the cards. Takes the argument 'number_of_decks'
        to determine the amount of decks to pick cards from.
        """
        # Code referenced from here:
        # https://www.geeksforgeeks.org/how-to-print-a-deck-of-cards-in-python/
        # Code has been changed slightly to fit this function

        # A temporary deck is created in order to not risk overwriting any
        # existing deck variable. This will be returned
        # at the end of the function.
        temp_deck = []
        for i in range(number_of_decks):
            for suit in suits:
                for rank in ranks:
                    temp_deck.append(rank + suit)
        return temp_deck

    def card_draw():
        '''
        Called when a random card should be drawn.
        Returns the card.
        '''

        card = random.choice(deck)
        # Removes the card from the deck
        deck.remove(card)

        return card

    def calc_value(cards, card_value):
        '''Calculates the value of a set of cards'''

        includes_ace = False
        total_value = 0
        for i in cards:
            # Removes the last character in the card, aka the suit
            rank = i[:-1]
            # If an Ace is found it turns the includes_ace var to True
            if (rank == "A"):
                includes_ace = True
            value = card_value[rank]
            total_value = total_value + value

        # If the value exceeds 21 and the cards include an ace, the ace
        # will count as a 1 instead of 11. This is done by removing
        # 10 from the total value
        if (total_value > highest_value and includes_ace):
            total_value = total_value - 10

        return total_value

    def save_game(username):
        '''Saves the amount of credits the user has'''
        db["player"].update_one({"username": username},
                                {"$set": {"balance": balance}})

    def get_saved_game(username):
        '''Gets any save info the player has'''
        # Tells the game to use the global variable "balance"
        global balance
        # First get's a dict of the information in the database entry
        # Then it picks the value with the key "balance"
        balance = db["player"].find_one({"username": username})
        balance = balance["balance"]


# Functions
def connect_to_DB():
    '''Connect to the MongoDB database'''
    # Load the .env file before anything else
    load_dotenv()

    # Get database credentials and create connection to database
    DBCREDS = os.getenv('DBCREDS') + "=true&w=majority"
    # Makes the variables global for future use
    global db_client
    db_client = MongoClient(DBCREDS, server_api=ServerApi('1'))
    global db
    db = db_client["blackjack"]

    # Try if the database can be accessed.
    # Otherwise print the error to the console.
    try:
        db_client.admin.command('ping')
    except Exception as e:
        print("Database exception:", e)


def print_board(stand, player_cards, dealer_cards):
    '''
    Prints the board. Stand = if the dealer should reveal their hidden card,
    ie if the player has decided to stand or has bust
    '''
    # Starts by clearing the terminal
    os.system('clear')

    player_cards_value = game.calc_value(player_cards, card_value)
    dealer_up_card = dealer_cards[0]

    # If the player has decided to stand or has bust the dealers
    # down card will be revealed
    if (stand is True):
        # If the player has decided to stand the dealer will show both cards
        # And the value of both cards will be calculated
        dealer_shown_cards = dealer_cards
        dealer_cards_value = game.calc_value(dealer_cards, card_value)
    else:
        # If the player has not decided to stand yet one of the
        # Dealers cards is hidden and only the shown card's value is calculated
        dealer_shown_cards = ["?", dealer_up_card]
        dealer_cards_value = game.calc_value([dealer_up_card], card_value)

    # Makes the cards display as a string instead of a list
    dealer_cards_clean = ""
    player_cards_clean = ""

    # Adds the cards to a string to ommit the square brackets and quotes
    # you get When printing a list
    for card in dealer_shown_cards:
        # Encase the card in a pair of lines
        card_clean = " |" + card + "| "
        dealer_cards_clean = dealer_cards_clean + card_clean

    for card in player_cards:
        # Encase the card in a pair of lines
        card_clean = " |" + card + "| "
        player_cards_clean = player_cards_clean + card_clean

    # Prints the values to the console
    print("Dealers cards:", dealer_cards_clean)
    print("Dealers cards value:", dealer_cards_value)
    print()
    print("Players cards:", player_cards_clean)
    print("Player cards value:", player_cards_value)
    print()
    print("Cards left:", len(deck))


def custom_deck():
    '''
    Let's the user choose how many decks to play with
    Many casinos use multiple decks to throw off certain strategies
    '''
    # The code loops until a valid value has been put in
    # ans = the user's input. Short for answer
    while True:
        try:
            print("Casinos typically use multiple decks for more"
                  " cards to pick from. Default is 6. \n"
                  "Type Cancel or C to cancel. This will select the default")
            ans = input("How many decks?: ")
            # .lower() is used to make the if statement case insensitive
            if (ans.lower() == "cancel" or ans.lower() == "c"):
                return game.generate_deck(6)
            else:
                # If the player chooses a number below 1 it
                # loops back to the start
                ans = int(ans)
                if (int(ans) < 1):
                    print(f"You can't play with {ans} number of decks."
                          " Choose a number that is at least 1.")
                    continue
                else:
                    # If everything goes through the function returns the deck
                    return game.generate_deck(ans)
        except ValueError:
            # The error will most likely be a variable type
            # conversion error
            print("Input has to be a number.")
            # The code will loop back to the begginning of the loop
            continue


def login_or_create():
    '''
    Prompts the user to either log in or create an account.
    Loops until the user has logged in or created an account
    '''
    while True:
        # Tells the function to use the global variable "username"
        global username
        # ans = the users answer
        ans = input("Login or Create account?: \n"
                    "Options: \n - login \n - create \n").lower()

        # If either the username or password does not equal "unsuccessful"
        # the user has logged in/created an account and the loop breaks
        # Otherwise it loops back to the start, asking the user if they want
        # To log in or create an account
        if ans == "login":
            username = account.log_in()
            if username != "unsuccessful":
                break
        elif ans == "create":
            username = account.create_account()
            if username != "unsuccessful":
                break
        else:
            print("Invalid choice")


def game_setup():
    '''Gives the player and dealers their cards'''
    # Empty lists to append to
    player_cards = []
    dealer_cards = []

    # The player recieves their cards
    for i in range(2):
        player_cards.append(game.card_draw())

    # The dealer recieves their cards
    for i in range(2):
        dealer_cards.append(game.card_draw())

    return player_cards, dealer_cards


def card_check(timeframe):
    '''
    Checks if there's enough cards to continue playing
    timeframe = at which point in the game the function is called
    '''
    # Tells the function to use the global variable "deck"
    global deck
    # Cards cannot be dealt at the start if theres less than 4 cards left
    # In any other timeframe of the game there only needs to be one card left
    # If the deck does not have enough cards the user will be prompted to
    # enter a number of decks again
    if (len(deck) < 4 and timeframe == "start"):
        print("Out of cards. Restocking deck.")
        deck = custom_deck()
    elif (len(deck) < 1):
        deck = custom_deck()


def intro():
    '''The intro to the game'''
    # The ASCII art itself is stored in a txt file
    intro_text = open("./intro.txt", "r")
    print(intro_text.read())
    print()
    # Wait for the users input before clearing the screen
    input("Press enter to continue..")
    os.system("clear")


def tutorial():
    '''If the player doesn't know how to play this will be run'''

    # Ask the user if they know how to play until a valid answer is given
    # If "y", the loop will break
    # If "n" the tutorial text file will be printed to the console.
    # .lower() is used for case insensitivity
    while True:
        ans = input("Do you know how to play? Y/N: \n").lower()
        if (ans == "n"):
            tutorial_text = open("./tutorial.txt", "r")
            print(tutorial_text.read())
            input("Press enter to continue..")
            break
        elif (ans == "y"):
            break
        else:
            print("invalid choice")


def game_start():
    '''
    The game starts here
    '''
    # Start by clearing the console
    os.system("clear")
    # Tells the function to use the global variable "deck"
    global balance
    global deck

    # Ask the user for how many decks they want to play with
    deck = custom_deck()

    while True:

        if (balance <= 0):
            print("Out of credits. Balance has been set to 100 to give you "
                  "another chance.")
            balance = 100

        while True:
            bet = input(f"You have {balance} amount of credits left. \n"
                        "how much will you bet? \n")

            # Validates the input. If an error occurs it is most likely due
            # to a failed conversion from string to integer, most likely due to
            # the input not being a number or containing decimals
            try:
                bet = int(bet)
                # Makes sure the player can't bet more than they have
                if (bet > balance):
                    print("You can't bet more than you have.")
                else:
                    break
            except ValueError:
                print("Bet has to be a whole number")

        # Clear the console before the actual game starts
        os.system("clear")

        stand = False
        bust = False

        # Checks if the deck has more than 4 cards at the start
        card_check("start")
        game_cards = game_setup()

        # game_cards returns two lists. Separates these into two vars
        player_cards = game_cards[0]
        dealer_cards = game_cards[1]

        # Prints the board before the player get's to decide anything
        print_board(stand, player_cards, dealer_cards)

        # Starts by checking if the two first cards equals 21. This is
        # called a blackjack and it gives you 1.5x your bet back.
        # Since the script does not remove from the balance until a
        # win/loss has been achieved it gives back half of the entered value
        # In a real casino you would typically be given back the chip you
        # handed over plus your winnings
        if game.calc_value(player_cards, card_value) == highest_value:
            # Rounds the number to prevent decimals
            balance = balance + round(bet / 2)
            stand = True
            print("Blackjack! You won 1.5x your bet back. \n"
                  f"Current Balance: {balance}")

        # The player will be presented with a choice so long they haven't
        # decided to stand and so long they haven't bust.
        while stand is False:
            # "midpoint" doesn't actually do anything. It's put in as
            # an argument is mandatory
            card_check("midpoint")

            # ans is short for answer. .lower() is used to make the
            # variable lowercase, essentially making the answer case
            # insensitive
            ans = input("Hit or stand?: ").lower()
            if ans == "hit":
                # If the player hits a card will be drawn and
                # added to the players hand
                card = game.card_draw()
                player_cards.append(card)

                # If the player hits and their hand exceeds 21 they will
                # automatically lose
                if (game.calc_value(player_cards, card_value) > highest_value):
                    stand = True
                    bust = True
            elif ans == "stand":
                stand = True

            # The board is updated
            print_board(stand, player_cards, dealer_cards)

        # If the player hasn't bust and the dealer has a value below
        # 17, the dealer has to pick up cards until it reaches at least 17
        while bust is False:
            if game.calc_value(dealer_cards, card_value) < 17:
                dealer_cards.append(game.card_draw())
            else:
                break

        # Update the board again
        print_board(stand, player_cards, dealer_cards)

        # After a terminal state has been reached the player and dealer
        # value will be calculated and compared
        dealer_value = game.calc_value(dealer_cards, card_value)
        player_value = game.calc_value(player_cards, card_value)

        # If the game is a draw the player's balance is not affected
        # If the dealer wins or the player busts the bet is
        # removed from the players balance
        # If the player wins or the dealer busts the bet is
        # added to the players balance.
        if (dealer_value == player_value):
            print(
                f"Draw. Your bet has been returned.\n"
                "Current balance: {balance}")
        elif (dealer_value > player_value and dealer_value <= highest_value):
            balance = balance - bet
            print(f"You lost. \nCurrent balance: {balance}")
        elif (bust):
            balance = balance - bet
            print(f"You bust. \nCurrent balance: {balance}")
        elif (dealer_value < player_value or dealer_value > highest_value):
            balance = balance + bet
            print(f"You won! \nCurrent balance: {balance}")

        # Saves the game and then waits for user input before clearing screen
        game.save_game(username)
        input("Press enter to continue..")
        os.system("clear")


# Main
intro()
tutorial()
# Clear the console before prompting for a login
os.system("clear")
print("Loading database, this might take a few seconds..")
connect_to_DB()
login_or_create()
game_start()
