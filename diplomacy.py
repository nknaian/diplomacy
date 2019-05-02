### Description: ###
# This program will take in 5 - 7 players inputs of up to 3 players
# that the player wants to meet with in a round. And it also takes
# as input that person's current number of cities. The program will
# return 3 rounds of meeting combinations that take into  account the
# players' choices and  number of cities

### Imports ###
import argparse

### Constants ###
MIN_NUM_PLAYERS = 5
MAX_NUM_PLAYERS = 7

### Exceptions ###

class PlayerInputError(Exception):
    pass

### Object Classes ###

class PlayerInfo:
    def __init__(self):
        self.choices = {}
        self.num_cities = None

class Players:

    def __init__(self):
        # Parse player names to create self.dictionary
        parser = argparse.ArgumentParser(description='Process player names')
        parser.add_argument('players', nargs='+', help='List of players')
        args = parser.parse_args()
        player_list = args.players

        # Thow input error if player_list is too short or long
        try:
            if (len(player_list) < MIN_NUM_PLAYERS) or (len(player_list) > MAX_NUM_PLAYERS):
                raise PlayerInputError("Must enter between {} and {} players".format(MIN_NUM_PLAYERS, MAX_NUM_PLAYERS))

        except PlayerInputError as error_message:
            print("Player Input Error: ", error_message)

        else:
            # Create empty dictionary to story players
            self.dict = {}
            for player_name in player_list:
                self.dict[player_name] = PlayerInfo()

            # Get choices and num_cities for each player
            for player_name, player_info in self.dict.items():
                player_info.choices = self.getChoicesFromInput(player_name)
                player_info.num_cities = self.getNumCitiesFromInput(player_name)

    # Take input choices from player. Continue trying until entered correctly
    def getChoicesFromInput(self, player):
        success = False
        while success == False:
            input_choices = input("Enter " + player + "\'s choices: ")
            input_choices = input_choices.replace(" ", "")
            choices = input_choices.split(",")
            try:
                # Make sure all names are in the dictionary
                if any((choice not in self.dict) for choice in choices):
                    print("choices = ", choices)
                    raise PlayerInputError("Player choice is unknown. Try again.")
                # Make sure no more than three choices are made
                elif len(choices) > 3:
                    raise PlayerInputError("Too many choices. Try again.")
                # Make sure no names are repeated
                elif len(choices) != len(set(choices)):
                    raise PlayerInputError("Player name repeated. Try again.")
                # Make sure the player didn't chose themself
                elif any((choice == player) for choice in choices):
                    raise PlayerInputError("Can't choose yourself! Try again.")
                else:
                    success = True
            except PlayerInputError as error_message:
                print("Player Input Error: ", error_message)
                success = False

        return choices

    # Take input num_cities from player. Continue trying until entered correctly
    def getNumCitiesFromInput(self, player):
        success = False
        while(not success):
            num_cities_string = input("Enter " + player + "\'s number of cities: ")
            try:
                if not num_cities_string.isdigit():
                    raise PlayerInputError("Number not entered. Try again")
                else:
                    success = True
            except PlayerInputError as error_message:
                print("Player Input Error: ", error_message)
                success = False

        return int(num_cities_string)

    # Print a readable display of the player dictionary
    def printDict(self):
        for player_name, player_info in self.dict.items():
            print(player_name, ":\n\tchoices = ", player_info.choices, "\n\tnumber of cities: ", player_info.num_cities)

### Main ###

if __name__ == "__main__":
    players = Players()
    players.printDict()
