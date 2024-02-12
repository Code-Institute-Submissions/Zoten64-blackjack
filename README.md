# Blackjack in a Python console

## [Link to website](https://zoten64-blackjack-f933aa260542.herokuapp.com/)

## Table of Contents:

* [Goals and target audience](#goals-and-target-audience)
* [User stories](#user-stories)
* [Features](#features)
* [Bugs and fixes](#bugs-and-fixes)
* [Technologies and tools](#technologies-and-tools)
* [Validation and testing](#validation-and-testing)
* [Deployment](#deployment)
* [Credits](#credits)

## Goals and target audience



## User stories


## Features


## Bugs and fixes

| Bug  | Fix |
| ------------- | ------------- |
| Entered username is always taken according to the script | True and False statements were mixed up |
| Credentials in the .env file keeps on getting messed up on import as it removes vital options | Delete options from the .env file and append them to the DBCREDS string in run.py. The options are not sensitive information |
| The password part of the create_account function runs despite create_username returning "interrupted"  | "interrupted" was misspelt as "inerrupted"|
| Script always outputs that the number of decks needs to be a number despite a number being put in | The conversion to int was not proper. int(ans > 0) instead of int(ans) > 0 making it try and compare a string and an integer before converting to an integer|
| String does not convert to int | Convert the string before the if statement |
| "c" for cancel does not work | Missing () after .lower |
| "cannot access local variable 'balance' where it is not associated with a value" error on a global variable| Declare the variable as global inside function |
| Player wins when the dealer should | accidentally used ">" instead of "<" |
| Player/dealer still bust even if value does not exceed 21 when cards include an Ace due to an Ace counting as 1 when the total value exceeds 21 when the Ace is worth 11 | Change the way the value is calculated by removing 10 when the total value exceeds 21 and there is an ace in the deck | 
| Dealer wins even though they have bust if their card value is higher than the players | Add additional check to make sure the dealer can't win if they bust |

## Technologies and tools
**Languages**
- Python

**Tools**
- Git/github
- Heroku
- Visual Studio Code
- Pip
- MongoDB
- [ASCII Art generator](https://patorjk.com/software/taag/)

**Python Libraries**
- Random
- OS
- Python-dotenv
- pymongo
- dnspython
- pwinput
- bcrypt



## Validation and testing
**Python**


**Wave accessibility**



**Lighthouse performance**



**Other tests**
<br>

**Browsers tested**



<br>

**Testing Devices**



<br>

**Testing user stories**

## Deployment

**Deploying and accessing the website**


**How to fork the project**

- Navigate to the github repository (You're probably here already)
- In the right corner click fork and choose a name

**How to clone the project**

Prerequisities:

- Have git downloaded and configured

steps:

- Go to the repository (You're probably here already)
- Click the code button
- Copy the url
- Open git and change the directory to the parent directory that you want the project to clone to
- Write "git clone [the link you just copied]", in this case "git clone https://github.com/Zoten64/blackjack.git"

## Credits
