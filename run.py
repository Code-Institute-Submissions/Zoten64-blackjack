# Import statements
import random
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load the .env file before anything else
load_dotenv()


# Global variables
# Get database credentials and create connection to database
DBCREDS = os.getenv('DATABASECREDS')
client = MongoClient(DBCREDS, server_api=ServerApi('1'))
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


def test_database_connection():
    """
    Tests the database connection for any errors
    """
    try:
        client.admin.command('ping')
        print("Database connected")
    except Exception as e:
        print("Database exception:", e)

test_database_connection()