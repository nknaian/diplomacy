### Description: ###
# Helpful classes and functions for the whole diplomacy project

### Imports ###

from random import randint

### Exceptions ###

class PlayerInputError(Exception):
    pass

### Helper Functions ###

def pickRandomEntryFromList(list):
    random_selection = randint(0, len(list) - 1)
    return list[random_selection]

def getOverlapBetweenLists(list1, list2):
    return list(set(list1) & set(list2))
