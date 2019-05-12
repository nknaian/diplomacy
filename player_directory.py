### Description: ###
# Player directory

### Imports ###

import copy
import json

import utils
import player as p
import meeting_slot as ms

### Player Directory Class ###
class PlayerDirectory:

    ### Constants ###

    MIN_NUM_PLAYERS = 5
    MAX_NUM_PLAYERS = 7
    NUM_MEETINGS = 3
    MAX_GROUP_SIZE = 3
    MAX_NUM_CITIES = 18

    ### INITIALIZATION FUNCTIONS ###

    def __init__(self, command_line_input):
        # Initialize members
        self.player_directory = {}
        self.meeting_schedule = []

        # Get player info input
        self.readPlayersFromInput(command_line_input)

        # Narrow down players' choices by comparing lists
        self.narrowChoices()

        # Initialize meetings schedule
        for i in range(0, self.NUM_MEETINGS):
            self.meeting_schedule.append(ms.MeetingSlot())

    def readPlayersFromInput(self, command_line_input):
        # Create player_list and json_player_input_dict if json option was used. Throw
        # error if there was a problem in the command line input
        json_player_input_dict = None
        player_list = []
        try:
            if command_line_input.players != None and command_line_input.json != None:
                raise utils.PlayerInputError("Can only specify one input source. Either --json or --players")
            elif command_line_input.players != None:
                player_list = command_line_input.players
            elif command_line_input.json != None:
                with open(command_line_input.json) as jsonFile:
                    json_player_input_dict = json.load(jsonFile)
                for player_name, player_info in json_player_input_dict.items():
                    player_list.append(player_name)
            else:
                raise utils.PlayerInputError("Must enter either --players or --json")

            if (len(player_list) < self.MIN_NUM_PLAYERS) or (len(player_list) > self.MAX_NUM_PLAYERS):
                raise utils.PlayerInputError("Must enter between {} and {} players".format(self.MIN_NUM_PLAYERS, self.MAX_NUM_PLAYERS))

        except utils.PlayerInputError as error_message:
            raise error_message

        # Create empty dictionary to story input
        for player_name in player_list:
            self.player_directory[player_name] = p.Player(player_name)

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

            except utils.PlayerInputError as error_message:
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
        for i in range(0, self.NUM_MEETINGS):
            print("\n\nCalculating meeting slot {}...".format(i+1))

            unbooked_players = player_list
            while len(unbooked_players) > self.MAX_GROUP_SIZE:
                # Take player with fewest cities and least matches. And make match with that person
                # update unbooked_players
                meeting_match = self.determineMeetingMatch(unbooked_players)
                if meeting_match:
                    self.meeting_schedule[i].addGroup(meeting_match)
                else:
                    # No one wanted each other, so just put all the remaining players in a room together
                    print("\n\nGuess no one wanted to meet...")
                    print("\nHere's what their choices look like right now:\n")
                    self.printPlayerDirectory(unbooked_players)
                    break
                unbooked_players = list(set(player_list) - set(self.meeting_schedule[i].getBookedPlayers()))

            # Now make a group with the remaining unbooked players
            self.meeting_schedule[i].addGroup(unbooked_players)
            print("\n\nWell, now {} are stuck together.".format(unbooked_players))

            print("\n\nDone.")

    # Print a readable display player_directory. Can input a subset of players to print
    def printPlayerDirectory(self, player_subset=None):
        if player_subset is None:
            player_subset = list(self.player_directory.keys())
        for player_name, player_info in self.player_directory.items():
            if player_name in player_subset:
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
                choice_maker = utils.pickRandomEntryFromList(possible_choice_makers)
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
                print("\n\n{} choses {} automatically".format(choice_maker, choice))

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
        fewest_cities = {"players": [], "value": self.MAX_NUM_CITIES}
        fewest_meeting_choices = {"players": [], "value": self.NUM_MEETINGS}
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
        fewest_meeting_choices_and_cities = utils.getOverlapBetweenLists(fewest_meeting_choices["players"], fewest_cities["players"])
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
                    raise utils.PlayerInputError("Player is not one of the possible matches. Try again.")

            except utils.PlayerInputError as error_message:
                print("utils.PlayerInputError: ", error_message)
