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
default_card_value = {
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
card_value = default_card_value
highest_value = 21
dealers_score = 0
players_score = 0
credits = 1000
deck_count = 1
global deck


# Functions

def connect_to_DB():
    '''Connect to the MongoDB database'''
    # Load the .env file before anything else
    load_dotenv()

    # Get database credentials and create connection to database
    DBCREDS = os.getenv('DBCREDS') + "=true&w=majority"
    global db_client
    db_client = MongoClient(DBCREDS, server_api=ServerApi('1'))
    global db
    db = db_client["blackjack"]

    # Try if the database can be accessed
    try:
        db_client.admin.command('ping')
        print("Database connected")
    except Exception as e:
        print("Database exception:", e)

# Objects/classes


class account:
    '''Account related functions'''
    def try_again(prompt):
        '''
        The user will be asked if they want to try again
        The prompt variable will be printed making this code reuseable
        '''

        ans = input(prompt).lower()
        if (ans == "y"):
            return True
        elif (ans == "n"):
            return False
        else:
            print("Invalid option.")

    def create_account():
        '''Create an account and put it into the database'''
        # Username or Password will equal "interrupted" if the user cancels
        # either of the retries when an input is invalid
        # In this case return makes the function stop running
        username = account.create_username()
        if (username == "interrupted"):
            return

        password = account.create_password()
        if (password == "interrupted"):
            return
        else:
            # The data is made into a dictionary and put into the db
            data = {"username": username, "password": password}
            db["player"].insert_one(data)
            return "success"

    def create_username():
        '''Lets user create a username'''

        # Repeats until an available username is found or the user cancels
        # If an available username is found it returns it
        # If the user cancels the function will return "interrupted"
        while True:
            username = input("username: ")
            if account.username_exists(username):
                if (account.try_again("Username is taken. Try again? Y/N: ")
                        == False):
                    return "interrupted"
            else:
                return username

    def create_password():
        '''Lets user create a password'''
        # This will loop until the passwords matches or the user cancels
        # Pwinput is used here to make the password hidden when the
        # user is typing it
        while True:
            password = pwinput.pwinput(prompt="Password: ", mask="*")
            password_confirm = pwinput.pwinput(prompt="Confirm password: ",
                                               mask="*")

            if (password == password_confirm):
                return account.hash_password(password)
            else:
                if (account.try_again("Passwords do not match. "
                                      "Try again? Y/N: ") == False):
                    return "interrupted"

    # Both hash and check password functions reference this tutorial:
    # https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt/

    def hash_password(password):
        '''Hashes the password'''
        # Converts the password to bytes
        bytes = password.encode("utf-8")
        # Generates salt for a more secure encryption
        salt = bcrypt.gensalt()
        # Finally hashes the password
        hash = bcrypt.hashpw(bytes, salt)

        return hash

    def username_exists(username):
        '''Checks if a username exists'''
        # Counts the amount of documents containing the username.
        # If the amount is not 0 the username is taken
        if (db["player"].count_documents({"username": username})) == 0:
            return False
        else:
            return True

    def check_password(password, username):
        '''Checks if the password is correct'''
        # Converts the password into bytes
        bytes = password.encode("utf-8")
        hash = db["player"].find_one({"username": username},
                                     {"password": True})["password"]
        # Checks if the password matches
        if (bcrypt.checkpw(bytes, hash)):
            return True
        else:
            return False

    def log_in():
        '''Prompts the user for login information'''
        while True:
            username = input("Username: ")
            # If the username does not exist this will run
            if account.username_exists(username) == False:
                # If the username is invalid the user will be prompted
                # to try again or cancel
                if (account.try_again("invalid username. Try again? Y/N: ")
                        == False):
                    break
                else:
                    # Makes it loop back to the start
                    continue

            while True:
                password = pwinput.pwinput(prompt="Password: ", mask="*")
                account.check_password(password, username)
                if (account.check_password(password, username)):
                    print(f"Welcome {username}.")
                    break
                else:
                    if (account.try_again("invalid password. Try again? Y/N: ")
                            == False):
                        break
                    else:
                        # Makes it loop back to the start
                        continue
            # If everything goes through the function returns the username
            return username
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
        Called when a card should be drawn
        '''
        card = random.choice(deck)
        deck.remove(card)

        return card
    
    def calc_value(cards, card_value):
        '''Calculates the value of a set of cards'''
        total_value = 0
        for i in cards:
            #Removes the last character in the card, aka the suit
            rank = i[:-1]
            value = card_value[rank]
            total_value = total_value + value
        return total_value
    


    

# Functions
        
def print_board(state, cards, deck):
    '''
    Prints the board. The cards var requires a list where [0] is the
    player's cards and [1] is the dealers cards. State = if the dealer
    should reveal their hidden card, ie if the player has decided to stand
    '''

    player_cards = cards[0]
    dealer_cards = cards[1]

    dealer_up_card = dealer_cards[0]
    dealer_hidden_card = dealer_cards[1]

    #if state = True the player has decided to stand
    if(state == True):
        dealer_shown_cards = [dealer_hidden_card, dealer_up_card]
    else:
        dealer_shown_cards = ["?", dealer_up_card]
    
    print("Dealers cards:", dealer_shown_cards)
    print("Players cards:", player_cards)
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
                    "Type Cancel or C to cancel.")
            ans = input("How many decks?: ")
            # .lower() is used to make the if statement case insensitive
            if (ans.lower() == "cancel" or ans.lower() == "c"):
                break
            else:
                # If the player chooses a number below 1 it
                # loops back to the start
                ans = int(ans)
                if (int(ans) < 1):
                    print(f"You can't play with {ans} number of decks."
                            " Choose a number that is at least 1.")
                    continue
                else:
                    # If everything goes through the function
                    # will return the deck
                    return game.generate_deck(ans)
        except Exception as e:
            # The error will most likely be a variable type
            # conversion error
            print(e)
            print("Input has to be a number.")
            # The code will loop back to the begginning of the loop
            continue

def login_or_create():
    '''
    Asks the user if they want to create an account or log in. Loops
    until a valid answer has been given
    '''
    while True:
        ans = input("Login or Create account?: \n"
                    "Options: \n - login \n - create \n")
        
        if ans.lower() == "login":
            if account.log_in() != "unsuccessful":
                break
        elif ans.lower() == "create":
            if account.create_account() == "success":
                break
        else:
            print("Invalid choice")


# This code is temporary, but might be reused later
connect_to_DB()
login_or_create()


