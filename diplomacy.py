### Description: ###
# This program will take in 5 - 7 players inputs of up to 3 players
# that the player wants to meet with in a round. And it also takes
# as input that person's current number of cities. The program will
# return 3 rounds of meeting combinations that take into  account the
# players' choices and  number of cities

### Imports ###
import argparse
import json
import copy
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

### Helper Functions ###

def pickRandomPlayerFromList(player_list):
    random_selection = randint(0, len(player_list) - 1)
    return player_list[random_selection]

def getOverlapBetweenLists(list1, list2):
    return list(set(list1) & set(list2))

### Object Classes ###

class MeetingSlotInfo:
    ### INITIALIZATION FUNCTIONS ###

    def __init__(self):
        self.groups = []

    ### PUBLIC FUNCTIONS ###

    def addGroup(self, player_group):
        self.groups.append(player_group)

    def getBookedPlayers(self):
        booked_players = []
        for group in self.groups:
            booked_players.extend(group)
        return booked_players

    def printSlot(self):
        for i in range(0, len(self.groups)):
            print("\tGroup {}: {}".format(i+1, self.groups[i] ))

class PlayerInfo:
    ### INITIALIZATION FUNCTIONS ###

    def __init__(self, player_name):
        self.name = player_name
        self.choices = [] # TODO: rename this to player_choices
        self.num_cities = 0
        self.num_meeting_choices = 0

    ### PUBLIC FUNCTIONS ###

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

    # Get a list of choices for this player that overlap with a given list
    def getChoicesThatOverlapWithList(self, list):
        return getOverlapBetweenLists(self.choices, list)
class Players:

    ### INITIALIZATION FUNCTIONS ###

    def __init__(self):
        # Initialize members
        self.player_directory = {}
        self.meeting_schedule = []

        # Get player info input
        self.readPlayersFromInput()

        # Narrow down players' choices by comparing lists
        self.narrowChoices()

        # Initialize meetings schedule
        for i in range(0, NUM_MEETINGS):
            self.meeting_schedule.append(MeetingSlotInfo())

    def readPlayersFromInput(self):
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
            if args.players != None and args.json != None:
                raise PlayerInputError("Can only specify one input source. Either --json or --players")
            elif args.players != None:
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

        # Create empty dictionary to story input
        for player_name in player_list:
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

    # Narrow down the choices member in the players' info so that only matches are included
    def narrowChoices(self):
        # Iterate over a copy of the player directory so we can remove elements
        # from the real player directory while we iterate
        player_directory_copy = copy.deepcopy(self.player_directory)
        for player_name, player_info in player_directory_copy.items():
            for choice in player_info.choices:
                if player_name not in player_directory_copy[choice].choices:
                    # 'remove' removes the first matching value only, but
                    # we can safely use this because we know that player
                    # choices cannot be repeated
                    self.player_directory[player_name].choices.remove(choice)

    ### PUBLIC FUNCTIONS ###

    def determineMeetingSchedule(self):
        # Get full list of players
        player_list = list(self.player_directory.keys())

        # Build meeting list
        for i in range(0, NUM_MEETINGS):
            unbooked_players = player_list
            while len(unbooked_players) > MAX_GROUP_SIZE:
                # Take player with fewest cities and least matches. And make match with that person
                # update unbooked_players
                meeting_match = self.determineMeetingMatch(unbooked_players)
                if meeting_match:
                    self.meeting_schedule[i].addGroup(meeting_match)
                else:
                    # No one wanted each other, so just put all the remaining players in a room together
                    self.meeting_schedule[i].addGroup(unbooked_players)
                    break
                unbooked_players = list(set(player_list) - set(self.meeting_schedule[i].getBookedPlayers()))

            # Now make a group with the remaining unbooked players
            self.meeting_schedule[i].addGroup(unbooked_players)

    # Print a readable display of the input dictionary
    def printPlayerDirectory(self):
        for player_name, player_info in self.player_directory.items():
            print(player_name, ":\n\tchoices = ", player_info.choices, "\n\tnumber of cities: ", player_info.num_cities)

    def printMeetingSchedule(self):
        for i in range(0, len(self.meeting_schedule)):
            print("Meeting Slot {}:".format(i+1))
            self.meeting_schedule[i].printSlot()
            print("")

    ### PRIVATE FUNCTIONS ###

    def determineMeetingMatch(self, unbooked_players):
        possible_choice_makers = self.playersWhoCanMakeChoice(unbooked_players)

        # Determine choice maker from list
        meeting_match = []
        if possible_choice_makers:
            # Narrow down possible choice makers based on who needs it the most
            if len(possible_choice_makers) > 1:
                possible_choice_makers = self.playersInNeedOfMeetingChoice(possible_choice_makers)

            # If there are still multiple options, choose randomly
            if len(possible_choice_makers) > 1:
                choice_maker = pickRandomPlayerFromList(possible_choice_makers)
            else:
                choice_maker = possible_choice_makers[0]

            # Increment the choice_makers number of choices count
            self.player_directory[choice_maker].num_meeting_choices += 1

            # Figure out who the choice maker's possible matches
            possible_matches = self.player_directory[choice_maker].getChoicesThatOverlapWithList(unbooked_players)

            if len(possible_matches) > 1:
                choice = self.getChoiceFromChoiceMaker(choice_maker, possible_matches)
            else:
                choice = possible_matches[0]

            meeting_match = [choice_maker, choice]

        # Trim down the players choices now that a match has been made
        if meeting_match:
            self.player_directory[choice_maker].choices.remove(choice)
            self.player_directory[choice].choices.remove(choice_maker)

        return meeting_match

    # Return a list of the players in the unbooked_players list that still have choices
    def playersWhoCanMakeChoice(self, unbooked_players):
        possible_choice_makers = []
        for player_name, player_info in self.player_directory.items():
            if player_name in unbooked_players:
                if player_info.getChoicesThatOverlapWithList(unbooked_players):
                    possible_choice_makers.append(player_name)
        return possible_choice_makers

    # Find player/s most in need of a meeting choice (fewest meeting choices, fewest cities as tiebreaker)
    def playersInNeedOfMeetingChoice(self, possible_choice_makers):
        fewest_cities = {"players": [], "value": MAX_NUM_CITIES}
        fewest_meeting_choices = {"players": [], "value": NUM_MEETINGS}
        for player_name, player_info in self.player_directory.items():
            if player_name in possible_choice_makers:
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

        # return a list of the needist players that can make a choice
        fewest_meeting_choices_and_cities = getOverlapBetweenLists(fewest_meeting_choices["players"], fewest_cities["players"])
        if fewest_meeting_choices_and_cities:
            return fewest_meeting_choices_and_cities
        else:
            return fewest_meeting_choices["players"]

    def getChoiceFromChoiceMaker(self, choice_maker, possible_matches):
        print("\n\n{}, who would you like to meet with?\nOptions: {}".format(choice_maker, possible_matches))
        while True:
            try:
                choice = input("Choice: ")
                if choice in possible_matches:
                    return choice
                else:
                    raise PlayerInputError("Player is not one of the possible matches. Try again.")

            except PlayerInputError as error_message:
                print("PlayerInputError: ", error_message)

### Main ###

if __name__ == "__main__":
    try:
        # Initialize Players
        players = Players()

        # Print the player directory after choices have been narrowed
        print("\nPlayer information with choices narrowed:")
        players.printPlayerDirectory()

        # Determine the meeting schedule
        print("\n\nCalculating meeting schedule...")
        players.determineMeetingSchedule()
        print("\n\nDone calculating... Now printing out the meeting schedule: ")
        players.printMeetingSchedule()

    except PlayerInputError as error_message:
        raise error_message
    except Exception as error_message:
        raise error_message
