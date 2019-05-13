# Diplomacy

## Breif
Program to assist in determining the meeting schedule for the diplomatic phase of the boardgame diplomacy.

## Usage
python -m diplomacy --json player_directory.json
OR
python -m diplomacy --players name1 name 2 name 3 ..

## Description
### Determines the best meeting schedule for the diplomatic phase of diplomacy by using  
the following input information:
1. the players participating
2. Their choices for who the players want to meet with (up to 3)
3. The number of cities they currently possess
### Uses the following rules to determine the meeting matches:
1. Only players that have chosen each other can be matched together
2. Players who have had the fewest choices of who to match with in the 
current diplomatic choosing phase will have priority when determining whose choice 
to take into account next
3. Players who have the fewer cities than others will have priority when determiing
whose choice to take into account next
4. If there is a tie in who gets to choose, a player is chosen randomly
5. Once there are 3 players or fewer remaining unmatched, they all get put in a group 
together, and we move on to the next round of meetings

## Areas for improvement:
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
