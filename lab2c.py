"""
This mini project asked me to recreate the "Code Master" board game between the user and the computer. The premise of the game is that the user 
tries to figure out four random colors picked by the computer in the as little moves as possible.
"""

import random
import pytest

def make_random_code():
    """
    This function takes no arguments and retuns four random letters.

    Arguments: None
    Return Values: Four random letters from a list of letters
    """
    colors = ['R', 'G', 'B', 'Y', 'O', 'W']
    choice = []
    for i in range(len(colors)-2):
        choice.append(random.choice(colors))
    return choice

def count_exact_matches(str1, str2):
    """
    This function takes two strings of length four each and returns an int 
    number of places where the two strings have the exact same letters at the exact same locations

    Arguments: two string arguments 
    Return Values: an int representing the number of places where the two strings have the exact 
    same letters at the exact same locations
    """
    matches = 0
    count = 0
    for letter in str1:
        if letter == str2[count]:
            matches += 1
        count += 1
    return matches

def count_letter_matches(str1, str2):
    """
    This function takes in two string arguments and returns the number of charecters that
    the two strings share.

    Arguments: Two strings
    Return Value: int of the number of charecters the two str arguments share.
    """
    s1 = list(str1)
    s2 = list(str2)
    matches = 0
    for letter in str1:
        if letter in s2:
            matches += 1
            s2.remove(letter)
    return matches

def compare_codes(code, guess):
    """
    This function takes in two string arguments and returns the amount of exact matches, matches, and 
    mismatches between the two string in the form of a string.

    Arguments: two string arguments
    Return Value: a string denoting the number of exact matches, matches, and mismatches between the two strings

    """
    result = ''
    count_b = 0
    count_w = 0
    count_dash = 0
    b = count_exact_matches(code, guess)
    w = count_letter_matches(code, guess) - count_exact_matches(code, guess)
    dash= 4 - (b+w)
    while b > count_b:
        result += 'b'
        count_b +=1
    while w > count_w:
        result += 'w'
        count_w +=1
    while dash > count_dash:
        result += '-'
        count_dash +=1
    return result

def run_game():
    """
    This function takes no arguments and has no return value, but prints the number of exact matches, matches, and mismatches
    an how long it takes to get all exact matches.

    Argument: None
    Return Value: None

    This fuunction prints to the terminal the number of moves and the combination matches
    """
    print('New game')
    moves = 1
    secret_code = make_random_code()
    while 1 == 1:
        result = compare_codes(secret_code, input('Enter your guess: '))
        print('Result: {}'.format(result))
        if result == 'bbbb':
            print('Congratulations! You cracked the code in {} moves!'.format(moves))
            break
        else:
            moves += 1

