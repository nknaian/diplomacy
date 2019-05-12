### Description: ###
# Player class.

### Imports ###

import utils

### Player Class ###
class Player:

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
            except utils.PlayerInputError as error_message:
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
            except utils.PlayerInputError as error_message:
                print("Player Input Error: ", error_message)
                success = False

    # Raise a utils.PlayerInputError exception if there are any problems with the
    # player's entered choices. Otherwise, set choices
    def setChoices(self, choices, input_dict):
        # Make sure all names are in the dictionary
        if any((choice not in input_dict) for choice in choices):
            raise utils.PlayerInputError("Player choice is unknown. Try again.")
        # Make sure no more than three choices are made
        elif len(choices) > 3:
            raise utils.PlayerInputError("Too many choices. Try again.")
        # Make sure no names are repeated
        elif len(choices) != len(set(choices)):
            raise utils.PlayerInputError("Player name repeated. Try again.")
        # Make sure the player didn't chose themself
        elif any((choice == self.name) for choice in choices):
            raise utils.PlayerInputError("Can't choose yourself!")
        else:
            self.choices = choices

    # Raise a utils.PlayerInputError exception if there are any problems with the
    # player's entered number of cities. Otherwise, set num_cities
    def setNumCities(self, num_cities):
        if isinstance(num_cities, str):
            if not num_cities.isdigit():
                raise utils.PlayerInputError("Integer not entered for number of cities. Try again")
            else:
                num_cities = int(num_cities)
        elif not isinstance(num_cities, int):
            raise utils.PlayerInputError("Integer not entered for number of cities. Try again")

        if num_cities < 0:
            raise utils.PlayerInputError("Negative integer entered for number of cities. Try again")

        self.num_cities = num_cities

    # Get a list of choices for this player that overlap with a given list
    def getChoicesThatOverlapWithList(self, list):
        return utils.getOverlapBetweenLists(self.choices, list)
