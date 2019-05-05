### Description: ###
# This program will take in 5 - 7 players inputs of up to 3 players
# that the player wants to meet with in a round. And it also takes
# as input that person's current number of cities. The program will
# return 3 rounds of meeting combinations that take into  account the
# players' choices and  number of cities

### Imports ###
import argparse
import json

### Constants ###
MIN_NUM_PLAYERS = 5
MAX_NUM_PLAYERS = 7

### Exceptions ###

class PlayerInputError(Exception):
    pass

### Object Classes ###

class PlayerInfo:
    def __init__(self, player_name):
        self.name = player_name
        self.choices = {}
        self.num_cities = None

    # Take input choices from player. Continue trying until entered correctly
    def getChoicesFromInput(self, input_dict):
        success = False
        while success == False:
            input_choices = input("Enter " + self.name + "\'s choices: ")
            input_choices = input_choices.replace(" ", "")
            choices = input_choices.split(",")
            try:
                self.setChoices(choices, input_dict)
                success = True
            except PlayerInputError as error_message:
                print("Player Input Error: ", error_message)
                success = False

    # Take input num_cities from player. Continue trying until entered correctly
    def getNumCitiesFromInput(self):
        success = False
        while(not success):
            num_cities_string = input("Enter " + self.name + "\'s number of cities: ")
            try:
                self.setNumCities(num_cities_string)
                success = True
            except PlayerInputError as error_message:
                print("Player Input Error: ", error_message)
                success = False

    # Raise a PlayerInputError exception if there are any problems with the
    # player's entered choices. Otherwise, set choices
    def setChoices(self, choices, input_dict):
        # Make sure all names are in the dictionary
        if any((choice not in input_dict) for choice in choices):
            raise PlayerInputError("Player choice is unknown. Try again.")
        # Make sure no more than three choices are made
        elif len(choices) > 3:
            raise PlayerInputError("Too many choices. Try again.")
        # Make sure no names are repeated
        elif len(choices) != len(set(choices)):
            raise PlayerInputError("Player name repeated. Try again.")
        # Make sure the player didn't chose themself
        elif any((choice == self.name) for choice in choices):
            raise PlayerInputError("Can't choose yourself!")
        else:
            self.choices = choices

    # Raise a PlayerInputError exception if there are any problems with the
    # player's entered number of cities. Otherwise, set num_cities
    def setNumCities(self, num_cities):
        if isinstance(num_cities, str):
            if not num_cities.isdigit():
                raise PlayerInputError("Integer not entered for number of cities. Try again")
            else:
                num_cities = int(num_cities)
        elif not isinstance(num_cities, int):
            raise PlayerInputError("Integer not entered for number of cities. Try again")

        if num_cities < 0:
            raise PlayerInputError("Negative integer entered for number of cities. Try again")

        self.num_cities = num_cities

class Players:

    def __init__(self):

        # Parse command line input
        parser = argparse.ArgumentParser(description='Process player names')
        parser.add_argument('-p', '--players', nargs='+', help='List of players')
        parser.add_argument('-j', '--json', help='Json file with players dictionary')
        args = parser.parse_args()

        # Create player_list and json_player_input_dict if json option was used. Throw
        # error if there was a problem in the command line input
        json_player_input_dict = None
        player_list = []
        try:
            if args.players != None:
                player_list = args.players
            elif args.json != None:
                with open(args.json) as jsonFile:
                    json_player_input_dict = json.load(jsonFile)
                for player_name, player_info in json_player_input_dict.items():
                    player_list.append(player_name)
            else:
                raise PlayerInputError("Must enter either --players or --json")

            if (len(player_list) < MIN_NUM_PLAYERS) or (len(player_list) > MAX_NUM_PLAYERS):
                raise PlayerInputError("Must enter between {} and {} players".format(MIN_NUM_PLAYERS, MAX_NUM_PLAYERS))

        except PlayerInputError as error_message:
            raise error_message

        else:
            # Create empty dictionary to story input
            self.input_dict = {}
            for player_name in player_list:
                self.input_dict[player_name] = PlayerInfo(player_name)

            # Get choices and num_cities for each player
            if json_player_input_dict == None:
                for player_info in self.input_dict.values():
                    player_info.getChoicesFromInput(self.input_dict)
                    player_info.getNumCitiesFromInput()

            else:
                try:
                    for player_info in self.input_dict.values():
                        json_player_info = json_player_input_dict[player_info.name]

                        # Get choices from json and error check
                        player_info.setChoices(json_player_info["choices"], self.input_dict)

                        # Get num cities from json and error check
                        player_info.setNumCities(json_player_info["num_cities"])

                except PlayerInputError as error_message:
                    raise error_message

    # Print a readable display of the input dictionary
    def printInputDict(self):
        for player_name, player_info in self.input_dict.items():
            print(player_name, ":\n\tchoices = ", player_info.choices, "\n\tnumber of cities: ", player_info.num_cities)



### Main ###

if __name__ == "__main__":

    try:
        # Initialize Players
        players = Players()
    except PlayerInputError as error_message:
        print("PlayerInputError: ", error_message)
    else:
        # Print input dictionary
        players.printInputDict()
