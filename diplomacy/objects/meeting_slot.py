### Description: ###
# Meeting slot class. A slot represents one chunk of time where all players will
# have a meeting with either one or two other players

### Imports ###

import diplomacy.utils.helpers as helper
import diplomacy.utils.exceptions as exception

### Meeting Slot Class ###
class MeetingSlot:
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
