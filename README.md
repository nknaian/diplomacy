# diplomacy
Script to assist in playing the boardgame diplomacy

## Usage
Current usage is to assist in figuring out what the meeting schedule will be for
the diplomatic phase of a game of diplomacy. Call diplomacy.py with command line
input of either a json file as input or a list of player names. The input
information needed is the players participating and their player choices for
meetings, and the number of cities they currently possess. The program will
return a meeting schedule that takes into account the inputted player information.

## Areas for improvement:
0. Possible bug: I witnessed a case where in the second meeting slot, no one
wanted to meet with each other, but then meetings happened in the third...this
makes me think that some meetings could have happened in slot 2, but were
incorrectly filtered out
1. Change Player's self.player_directory into a list of PlayerInfo objects. Just
used PlayerInfo.name when the name is needed...that's why it's there
2. Pass around Player objects in functions instead of string lists that contain names...will be much less bug proof
3. Use function hints for argument types and return types
4. Add error checking to determineMeetingSchedule
5. Have output be json in addition to test in command line
6. Make a section (maybe a class, or maybe just a set of constants) that constitute
the rules it calculating the meeting schedule...so it will be more easily configurable
7. Make the number of meetings change based on how many players there are. I
believe this should allow for using this script with less than 5 participants.
8. Make a new class called MeetingSchedule, and  pull a bunch of stuff out of PlayerDirectory and put it in here
