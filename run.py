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
deck = []

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


def try_again(prompt):
    ans = input(prompt).lower()
    if(ans == "y"):
        return True
    elif(ans == "n"):
        return False
    else:
        print("Invalid option.")

def create_account():
    '''Create an account and put it into the database'''

    username = create_username()
    #Username will equal "interrupted" if the user cancels
    #In this case return makes the function stop running
    if(username == "interrupted"):
        return
    #This will loop until the passwords matches or the user cancels
    # Pwinput is used here to make the password hidden when the
    # user is typing it
    password = pwinput.pwinput(prompt="Password: ", mask="*")
    password_confirm = pwinput.pwinput(prompt="Confirm password: ", mask="*")
    
    #Makes sure that the passwords match before continuing
    if(password == password_confirm):
        hashed_pw = hash_password(password)
        # The data is made into a dictionary and put into the db
        data = {"username": username, "password": hashed_pw}
        db["player"].insert_one(data)




# Both password functions reference this tutorial:
# https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt/

def create_username():
    '''Checks for username availability.'''

    #Repeats until an available username is found or the user cancels
    while True:
        username = input("username: ")
        if username_exists(username) == True:
            ans = try_again("Username is taken. Try again? Y/N: ")
            if(ans == False):
                return "interrupted"
        else:
            return username
                

def hash_password(password):
    '''Hashes the password'''
    # Converts the password to bytes
    bytes = password.encode("utf-8")
    # Generates salt for a more secure encryption
    salt = bcrypt.gensalt()
    # Finally hashes the password
    hash = bcrypt.hashpw(bytes, salt)

    return hash


def check_password(password, hash):
    '''Checks if the password is correct'''
    # Converts the password into bytes
    bytes = password.encode("utf-8")
    # Checks if the password matches
    print(bcrypt.checkpw(bytes, hash))

def username_exists(username):
    '''Checks if a username exists'''
    #Counts the amount of documents containing the username.
    #If the amount is not 0 the username is taken
    if (db["player"].count_documents({"username": username})) == 0:
        return False
    else: 
        return True

def log_in():
    print("Non functional")


connect_to_DB()
create_account()
