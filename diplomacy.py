### Description: ###
# This program will take in 5 - 7 players inputs of up to 3 players
# that the player wants to meet with in a round. And it also takes
# as input that person's current number of cities. The program will
# return 3 rounds of meeting combinations that take into  account the
# players' choices and  number of cities

### Imports ###
import argparse
import json
from random import randint

### Constants ###
MIN_NUM_PLAYERS = 5
MAX_NUM_PLAYERS = 7
NUM_MEETINGS = 3
MAX_GROUP_SIZE = 3
MAX_NUM_CITIES = 18

### Exceptions ###

class PlayerInputError(Exception):
    pass

class CalculationError(Exception):
    pass

### Helper Functions ###

def pickRandomPlayerFromList(player_list):
    random_selection = randint(0, len(player_list))
    return player_list[random_selection]

### Object Classes ###

class PlayerInfo:
    def __init__(self, player_name):
        self.name = player_name
        self.choices = [] # TODO: rename this to player_choices
        #self.viable_choices = [] # TODO: Fill this instead of narrowing choices
        self.num_cities = 0
        self.num_meeting_choices = 0
        self.booked = []
        for i in range(0, NUM_MEETINGS):
            self.booked = False

    # TODO: Make property and setter decorator functions

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

    ### PUBLIC FUNCTIONS ###

    def __init__(self):

        # Parse command line input
        parser = argparse.ArgumentParser(description='Process player names')
        parser.add_argument('-p', '--players', nargs='+', help='List of players')
        parser.add_argument('-j', '--json', help='Json file with players dictionary')
        args = parser.parse_args()

        # Create player_list and json_player_input_dict if json option was used. Throw
        # error if there was a problem in the command line input
        json_player_input_dict = None
        self.player_list = []
        try:
            if args.players != None:
                self.player_list = args.players
            elif args.json != None:
                with open(args.json) as jsonFile:
                    json_player_input_dict = json.load(jsonFile)
                for player_name, player_info in json_player_input_dict.items():
                    self.player_list.append(player_name)
            else:
                raise PlayerInputError("Must enter either --players or --json")

            if (len(self.player_list) < MIN_NUM_PLAYERS) or (len(self.player_list) > MAX_NUM_PLAYERS):
                raise PlayerInputError("Must enter between {} and {} players".format(MIN_NUM_PLAYERS, MAX_NUM_PLAYERS))

        except PlayerInputError as error_message:
            raise error_message

        else:
            # Create empty dictionary to story input
            self.player_directory = {}
            for player_name in self.player_list:
                self.player_directory[player_name] = PlayerInfo(player_name)

            # Get choices and num_cities for each player
            if json_player_input_dict == None:
                for player_info in self.player_directory.values():
                    player_info.getChoicesFromInput(self.player_directory)
                    player_info.getNumCitiesFromInput()

            else:
                try:
                    for player_info in self.player_directory.values():
                        json_player_info = json_player_input_dict[player_info.name]

                        # Get choices from json and error check
                        player_info.setChoices(json_player_info["choices"], self.player_directory)

                        # Get num cities from json and error check
                        player_info.setNumCities(json_player_info["num_cities"])

                except PlayerInputError as error_message:
                    raise error_message

            # Narrow down players' choices by comparing lists
            self.narrowChoices()

            # Initialize meetings schedule
            self.meeting_schedule = {}
            for i in range(0, NUM_MEETINGS):
                self.meeting_schedule["Slot {}".format(i+1)] = {}

    def determineMeetingSchedule(self):

        # Build meeting list
        for i in range(0, NUM_MEETINGS):
            unbooked_players = self.player_list
            while unbooked_players > MAX_GROUP_SIZE:
                # Take player with fewest cities and least matches. And make match with that person
                # update unbooked_players
                unbooked_players = self.getUnbookedPlayers()


    # Print a readable display of the input dictionary
    def printPlayerDirectory(self):
        for player_name, player_info in self.player_directory.items():
            print(player_name, ":\n\tchoices = ", player_info.choices, "\n\tnumber of cities: ", player_info.num_cities)

    ### PRIVATE FUNCTIONS ###

    # Narrow down the choices member in the players' info so that only matches are included
    def narrowChoices(self):
        # Iterate over a copy of the player directory so we can remove elements
        # from the real player directory while we iterate
        player_directory_copy = self.player_directory
        for player_name, player_info in player_directory_copy.items():
            for choice in player_info.choices:
                if player_name not in self.player_directory[choice].choices:
                    # 'remove' removes the first matching value only, but
                    # we can safely use this because we know that player
                    # choices cannot be repeated
                    self.player_directory[player_name].remove(choice)


    def determineMeetingMatch(self, meeting_number, unbooked_players):
        possible_choice_makers = playersWhoCanMakeChoice(unbooked_players)
        possible_choice_makers = self.playersInNeedOfMatchChoice(possible_choice_makers)
        choice_maker = pickRandomPlayerFromList(possible_choice_makers)

    def getUnbookedPlayers(self, meeting_number):
        try:
            if meeting_number >= NUM_MEETINGS:
                raise CalculationError("Meeting number greater than number of meetings")
        except PlayerInputError as error_message:
            raise error_message
        else:
            unbooked_players = []
            for player_name, player_info in self.player_directory.items():
                if player_info.booked[meeting_number]:
                    unbooked_players.append(player_name)
            return unbooked_players

    # Find player/s that still
    def playersWhoCanMakeChoice(self, unbooked_players):
        possible_choice_makers = []
        for player_name, player_info in self.player_directory.items():
            if player_name in unbooked_players:
                if player_info.choices:
                    possible_choice_makers.append(player_name)
        return possible_choice_makers

    # Find player/s most in need of a meeting choice (fewest meeting choices, fewest cities as tiebreaker)
    def playersInNeedOfMeetingChoice(self, possible_choice_makers):
        fewest_cities = {"players": [], "value": MAX_NUM_CITIES}
        fewest_meeting_choices = {"players": [], "value": NUM_MEETINGS}
        for player_name, player_info in self.player_directory.items():
            if player_name in unbooked_players:
                # Determine whether player has fewest cities so far (or tied)
                if player_info.num_cities < fewest_cities["value"]:
                    fewest_cities["players"] = [player_name]
                    fewest_cities["value"] = player_info.num_cities
                elif player_info.num_cities <= fewest_cities["value"]:
                    fewest_cities["players"].append(player_name)

                # Determine whether player has fewest matches so far (or tied)
                if player_info.num_meeting_choices < fewest_meeting_choices["value"]:
                    fewest_meeting_choices["players"] = [player_name]
                    fewest_meeting_choices["value"] = player_info.num_meeting_choices
                elif player_info.num_meeting_choices <= fewest_meeting_choices["value"]:
                    fewest_meeting_choices["players"].append(player_name)






### Main ###

if __name__ == "__main__":

    try:
        # Initialize Players
        players = Players()

        # Print player directory
        players.printPlayerDirectory()

        # Determine the meeting schedule
        determineMeetingSchedule()

    except PlayerInputError as error_message:
        print("PlayerInputError: ", error_message)
    except CalculationError as error_message:
        print("CalculationError: ", error_message)
    except Exception as error_message:
        print("Error: ", error_message)
