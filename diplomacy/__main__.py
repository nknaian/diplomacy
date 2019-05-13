### Description: ###
# This program will take in 5 - 7 players inputs of
# up to 3 players that the player wants to meet with in a round. And it also
# takes as input that person's current number of cities. The program will
# return NUM_MEETINGS rounds of meeting combinations that take into
# account the players' choices and  number of cities

### Imports ###

import argparse

import diplomacy.utils.helpers as helper
import diplomacy.utils.exceptions as exception
import diplomacy.objects.player_directory as playerdir

### Main ###

if __name__ == "__main__":
    try:
        # Parse command line input
        parser = argparse.ArgumentParser(description='Process player names')
        parser.add_argument('-p', '--players', nargs='+', help='List of players')
        parser.add_argument('-j', '--json', help='Json file with players dictionary')
        args = parser.parse_args()

        # Initialize Players
        player_directory = playerdir.PlayerDirectory(args)

        # Print the player directory after choices have been narrowed
        print("\nPlayer information with choices narrowed:")
        player_directory.printPlayerDirectory()

        # Determine the meeting schedule
        player_directory.determineMeetingSchedule()

        # Print meeting schedule
        print("\n\nMeeting schedule:\n\n")
        player_directory.printMeetingSchedule()

    except utils.PlayerInputError as error_message:
        raise error_message
    except Exception as error_message:
        raise error_message
