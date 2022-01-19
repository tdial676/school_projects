"""
Thierno Diallo

This program ccreates a pokemon simulator and contains the numerous functions
required for interacting with our pokemon such as accessing and altering our 
pokemon index and our collected number of pokemon through renaming, adding,
and removing pokemon and more.
"""

import csv
from os.path import exists
from lab6_Pokemon import Pokedex, PokemonSpecies
from Move import Move

# Provided program constants
LVL_COEFFICIENT = 1.1  # hp stats -> (lvl * 1.1) + base hp
COLLECTED_COLUMNS = ['id', 'name', 'nickname', 'level',
                     'type', 'weakness', 'hp']


# C.1.
def load_moves():
    """
    Returns a dictionary mapping move names to
    Move objects based on data from moves.csv.
    Returns:
        `dict` mapping strings to Move objects.
    """
    moves = {}
    with open('moves.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            moves[row['move']] = Move(row['move'], row['type'], row['accuracy']
                                     , row['dp'], row['buff'], row['buff_amt'])
    return moves


# C.2.
def load_pokedex():
    """
    Loads Pokedex data from pokedex.csv and returns the result
    populated Pokedex object.
    Returns:
        `Pokedex` object
    """

    pokedex = Pokedex()
    moves_dic = load_moves()
    with open('pokedex.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pid = int(row['id'])
            name = row['name']
            desc = row['description']
            poke_type = row['type']
            weakness = row['weakness']
            hp = int(row['hp'])
            moves = []
            for move in ['move1', 'move2', 'move3', 'move4']:
                if row[move] != '':
                    moves.append(moves_dic[row[move]])
            pokemon = PokemonSpecies(pid, name, desc, poke_type,
                                     weakness, hp, moves)
            pokedex.add_pokemon(pokemon)
    return pokedex


# C.3.
def load_collected():
    """
    Returns a list of of pokemon objects from the the collected
    pokemon csv file.

    Arguments: None
    Return Value: a list of pokemon objects
    """
    collected_lst = []
    with open('collected.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            pid = int(row['id'])
            nickname = row['nickname']
            level = row['level']
            pokemon = pokedex.gen_pokemon(pid)
            pokemon.set_nickname(nickname)
            pokemon.set_level(level)
            collected_lst.append(pokemon)
    return collected_lst


# C.4.
def display_collected():
    """
    Takes no arguments and prints all the pokemon in the collected pokemon 
    list in the order they were added.

    Arguments: None
    Return Value: None
    """
    if len(collected) == 0:
        print('No Pokemon collected yet.')
    else:
        print('-' * 30)
        print('Your collected Pokemon:')
        print('-' * 30)
        for i, pokemon in enumerate(collected):
            print(f'{i + 1}: {pokemon}')   


# C.5.
def add_pokemon(pid):
    """
    Takes a pokeomon id and add the pokemon object with that pid to the 
    list of collected pokemon and prints a success message. Also, allows 
    the user the option to rename the added pokemon's nickname,
    if they want to.

    Arguments: int pid
    Return Value: None
    """
    pokemon = pokedex.gen_pokemon(pid)
    nickname = ''
    rename = input('Do you want to give a name to your new'
                   + f' {pokemon.name} (y for yes)? ')
    if rename.upper() == 'Y':
        while not nickname:
            nickname = input('What nickname do you want to give? ')
        else:
            pokemon.set_nickname(nickname)
    collected.append(pokemon)  
    print(f'Successfully added {pokemon.name} to collected!')      
    

# C.6.
def abandon_pokemon():
    """
    Prompts the user to choose a Pokemon they want to say goodbye to
    (removing it from their collected.csv Pokemon). A user cannot
    abandon their only Pokemon if they have only one left.
    If a user provides an invalid ID (less than 1 or greater than
    their collected count), prints an error message. Otherwise,
    prints a success message if successful.
    """
    display_collected()
    cid = input('Which Pokemon do you want to say goodbye to (Enter #)? ')
    cid = int(cid)
    if cid not in range(1, len(collected) + 1):
        print('Invalid entry given')
    elif len(collected) == 1:
        print('You\'re abandoning your only Pokemon!\n' +
        'You will have to reset your collected Pokemon if you want to do so.')
    else:
        print(f'Successfully said goodbye to {collected[cid-1].name}!')
        del collected[cid - 1]


# C.7.
def rename_pokemon(cid, new_name):
    """
    Renames a Pokemon using the given collected ID `cid` (int)
    to the given `new_name` (str).
    If cid is less than 1 or greater than the number
    of currently-collected Pokemon, outputs an error message.
    Otherwise, updates the managed collection appropriately
    and outputs a success message.
    """
    if cid not in range(1, len(collected) + 1):
        print('Invalid cid given')
    else:
        print(f'Successfully renamed {collected[cid - 1].nickname} to '
              + f'{new_name}!')
        collected[cid - 1].set_nickname(new_name)


# C.8. Utility Function
def collected_to_dict(pokemon):
    """
    Takes a pokemon object and returns a dictionarty representation of that
    pokemon.

    Arguments: a pokemon object
    Return Value: a dictionary representation of that pokemon
    """
    pokemon_dic = ({
                     'id': pokemon.id, 'name': pokemon.name,
                     'nickname': pokemon.nickname, 'level': pokemon.level,
                     'type': pokemon.type, 'weakness': pokemon.weakness, 
                     'hp': pokemon.curr_hp
                     })
    return pokemon_dic


# C.8. _Only_ File-Writing Function in Lab 6
def save_collected():
    """
    This function turns the collected pokemon object list into a list of 
    pokemon dictioraires and then writes those onto the collected csv file
    to save them. Then its prints a success message.

    Arguments: None
    Return Value: None
    """
    pokemon_lst = []
    for pokemon in collected:
       pokemon_lst.append(collected_to_dict(pokemon))
    with open('collected.csv', 'w', newline='') as cvs_file:
        writer = csv.DictWriter(cvs_file, fieldnames= COLLECTED_COLUMNS)
        writer.writeheader()
        writer.writerows(pokemon_lst)
    print('Successfully saved your collected Pokemon to collected.csv!')


def new_game():
    print('Game play unimplemented!')


# ---------------------------------------------------------------------------
# Setup Functionality
# ---------------------------------------------------------------------------
def assign_starter():
    """
    Randomly assigns a starter Pokemon managed by the Pokedex
    and adds it to the user's collection.
    The user has an option to give the Pokemon a nickname (defaulting)
    to the Pokemon's name in UPPERCASE if they don't want to.
    """
    pokemon = pokedex.gen_random_pokemon()
    name = pokemon.name
    print(f'Your new starter is {name}!')
    add_pokemon(pokemon.id)
    nickname = pokemon.nickname
    print('Successfully restarted your collected Pokemon with ' +
          f'your new starter {name} ("{nickname}")!')


def reset_collected():
    """
    Resets the collection.
    """
    with open('collected.csv', 'w') as f:
        f.write(','.join(COLLECTED_COLUMNS) + '\n')


# ---------------------------------------------------------------------------
# Provided UI Functionality
# ---------------------------------------------------------------------------
def show_options():
    print('What would you like to do?')
    print('  \'pokedex\' - View all Pokemon in the Pokedex')
    print('  \'collected\' - View all Pokemon you have collected')
    print('  \'add\' - Add a new Pokemon to your collection')
    print('  \'goodbye\' - Say goodbye to one of your collected Pokemon...')
    print('  \'reset\' - Reset your collected Pokemon with a new starter')
    print('  \'rename\' - Rename one of your collected Pokemon')
    print('  \'play\' - Start a new game')
    print('  \'test\' - Leave prompt for testing when using ' +
          '`python3 -i lab6c.py`')
    print('  \'q\' - Quit')
    print()
    option = input('Enter your option: ')
    if option:
        option = option.lower().strip()
    print()
    return option


def prompt_add_pokemon():
    """
    Prompts the user for a Pokedex ID to add a Pokemon to their collection.
    Note: This function is provided for students to quickly test their
    add_pokemon functionality without the gameplay implementation (in the
    completed version, Pokemon can only be added after defeating them
    in a Pokemon battle).
    """
    pokedex.display()
    while True:
        pid = input('Which Pokemon do you want to collect (enter an ID #)? ')
        if not pid.isnumeric():
            print('Please enter an ID # (as an integer): ')
        else:
            pid = int(pid)
            break
    add_pokemon(pid)


def prompt_clear_collected():
    """
    Prompts the user to confirm resetting their
    collection. Returns True if they confirm ('y' or 'Y')
    otherwise False.
    """
    confirm = input('Are you sure you want to erase all of ' +
                    'your collected data? ')
    if confirm.lower() == 'y':
        reset_collected()
        return True
    else:
        print('Aborting.')
        return False


def prompt_rename_pokemon():
    """
    Prompting functionality to rename a collected
    Pokemon.
    """
    print('Your collected Pokemon:')
    display_collected()
    cid = input('Which Pokemon would you like to rename? ')
    new_name = input('What is the new name you\'d like to give this Pokemon? ')
    rename_pokemon(int(cid), new_name)


def start_ui():
    """
    Starts the UI for the game, displaying options
    for a user involving Pokemon management and gameplay,
    as well as an option for testing purposes.
    """
    option = show_options()
    options = {'pokedex': None,
               'collected': display_collected,
               'add': prompt_add_pokemon,
               'reset': prompt_clear_collected,
               'goodbye': abandon_pokemon,
               'rename': prompt_rename_pokemon,
               'play': new_game,
               'test': None,
               'q': quit_game}
    while option not in options:
        print('Invalid option. Please enter an option listed.')
        option = show_options()
    if option == 'pokedex':
        pokedex.display()
    elif option == 'test':
        print('Leaving prompt for interactive testing mode.')
        return
    elif option == 'reset':
        if prompt_clear_collected():
            assign_starter()
    else:
        options[option]()

    print()
    reprompt = input('Do you want to do something else (y for yes)? ')
    if (reprompt.lower().startswith('y')):
        start_ui()
    else:
        save = input('Do you want to save your collection? ')
        if save.lower().startswith('y'):
            save_collected()
        quit_game()


def quit_game():
    """
    Prints a goodbye message and quits the program.
    """
    print('Good bye!')
    quit()


def main():
    """
    Starts the main menu after setting up collected
    dataset if one doesn't exist yet.
    """
    print('Welcome to the Pokemon Battle Simulator!')
    # Check for existence of collected.csv, if missing
    # reset and assign starter Pokemon
    if not exists('collected.csv'):
        reset_collected()
        assign_starter()
    start_ui()


if __name__ == '__main__':
    # These are both declared in global scope
    pokedex = load_pokedex()
    collected = load_collected()
    main()
