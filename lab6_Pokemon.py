"""
Thierno Diallo

Starter code for Lab 6, including implementations introduced in Lectures 22
and 23.

This program defines classes for Pokemon management, including
PokemonSpecies, Pokemon, and Pokedex.

Pokemon inherit from PokemonSpecies to represent Pokemon entities
with state unique to a Pokemon (e.g. nickname, level, curr_hp, and buffs).
Pokemon may be used for a player's collected Pokemon, or for
"wild" Pokemon that a player can battle against with their collected Pokemon
(and possibly add to their collection).

A Pokedex represents a collection of Pokemon species.
"""
# random will be used for a few random-generation of things like random moves
# or random Pokemon.
import random


class PokemonSpecies:
    """
    Represents a unique Pokemon species with the following attributes:
    id (int) - Pokedex ID # (e.g. 1 for Bulbasaur)
    name (str) - Name of Pokemon species
    type (str) - Type of Pokemon (e.g. 'Grass')
    weakness (str) - Weakness of Pokemon (e.g. 'Fire')
    moves (list) - List of Move objects. A Pokemon typically has 1-4 moves.
    description (str) - Description of the Pokemon.
    base_hp (int) - Base HP (health points) of a Pokemon.

    When Pokemon are collected, they can be represented as a Pokemon subclass.
    """

    def __init__(self, pid, name, desc, type, weakness, hp, moves):
        """
        Constructs a PokemonSpecies with the following arguments:
        `pid` (int) - Pokedex id for the PokemonSpecies `id` attribute
        `name` (str) - Name of the PokemonSpecies
        `desc` (str) - description of the PokemonSpecies for the
                       `description` attribute.
        `type` (str) - Type of the PokemonSpecies (e.g. 'Grass')
        `weakness` (str) - Weakness of the PokemonSpecies (e.g. 'Fire')
        `hp` (int) - "Health Point" value for the `base_hp` attribute
        `moves` (list) - List of Move objects known by the PokemonSpecies
        """
        self.id = int(pid)
        self.name = name
        self.description = desc
        self.type = type
        self.weakness = weakness
        self.base_hp = int(hp)
        self.moves = moves

    def __str__(self):
        """
        Returns a string representation of the PokemonSpecies in the format
        '#<id>: <name> (<pokemon type>)
        Example: '#1: Bulbasaur (Grass)'
        """
        return f'#{self.id}: {self.name} ({self.type})'
    
    def display_moves(self):
        """
        This method takes no arguments and prints each of the object's moves.

        Arguments: None
        Return Value: None
        """
        for move in self.moves:
            print(move)

    def get_move(self, move_name):
        """
        This method takes a move name argument and returns that move object 
        from the moves list matching that move name.

        Arguments: a str move_name
        Return Value: a move object
        """
        for move in self.moves:
            if move_name.upper() == move.name.upper():
                return move

    def get_random_move(self):
        """
        This method takes no arguments and returns a random move object from
        the list of moves.

        Arguments: None
        Return Value: a move object
        """
        return random.choice(self.moves)

    def is_weak_to(self, type):
        """
        This method takes a str pokemon type and returns a bool stating 
        whether the pokemon object is weak to that type.

        Argument: str type
        Return Value: A bool (True or False)
        """
        return self.weakness.upper() == type.upper()

class Pokedex:
    """
    Represents a Pokedex collection of unique PokemonSpecies with
    the following attribute:
        `all_pokemon` - dictionary mapping int ids to PokemonSpecies.
    """

    def __init__(self):
        """
        Constructs an empty Pokedex.
        """
        self.all_pokemon = {}

    def add_pokemon(self, pokemon):
        """
        Add the given PokemonSpecies to this Pokedex, mapping
        its id to the PokemonSpecies object. If given a pokemon
        with an id that is already saved in this Pokedex, prints
        an error message (the Pokedex is unchanged).
        """
        if pokemon.id in self.all_pokemon:
            print(f'Already have PokemonSpecies with given id {pokemon.id}')
        else:
            id = int(pokemon.id)
            self.all_pokemon[id] = pokemon

    def display(self):
        """
        Outputs the Pokedex information with a header and each
        PokemonSpecies's information in order of its id (with
        2-space indentation). Each Pokemon is printed using
        the default PokemonSpecies string representation.
        """
        print('-' * 30)
        print('Full Pokedex Information:')
        print('-' * 30)
        for pid in self.all_pokemon:
            print(f'  {self.all_pokemon[pid]}')

    def get_pokemon_data(self, pid):
        """
        This method takes a pokemon's int pid and returns the pokemon species
        object associated with that pid from the pokedex dictionary if 
        the pid exists.

        Arguments: an int pid
        Return Value: a pokemon sepecies object

        """
        if pid in self.all_pokemon:
            return self.all_pokemon[pid]
        else:
            print(f'Pokemon #{pid} not found.')

    def gen_pokemon(self, pid):
        """
        This method takes a pid and generates a new pokemon object
        based on the pokemon's info in the pokedex.

        Arguments: int pid
        Return Value: a pokemon object
        """
        if pid in self.all_pokemon:
            name = self.all_pokemon[pid].name
            desc = self.all_pokemon[pid].description
            type = self.all_pokemon[pid].type
            weakness = self.all_pokemon[pid].weakness
            hp = self.all_pokemon[pid].base_hp
            moves = self.all_pokemon[pid].moves
            return Pokemon(pid, name, desc, type, weakness, hp, moves)
        else:
            print(f'Pokemon #{pid} not found.')

    def gen_random_pokemon(self):
        """
        This method takes no arguments and returns a randomly generated
        pokemon object.

        Arguments: None
        Return Value: random pokemon object
        """
        return self.gen_pokemon(random.choice(list(self.all_pokemon.keys())))

class Pokemon(PokemonSpecies):
    """
    Represents a Pokemon entity inheriting properties and methods of a
    PokemonSpecies super class.
    Pokemon have additional attributes that may vary for different
    Pokemon objects of the same PokemonSpecies, including:
    `level` (int) - the level of the Pokemon between STARTER_LVL and MAX_LVL.
    `curr_hp` (int) - the current HP of a Pokemon between 0 and its base_hp.
                      A Pokemon is "fainted" if curr_hp is 0 (Pokemon never
                      "die" of course; that would unethical)
    `nickname` (str) - the nickname of a Pokemon which a player can change.
                       Defaults to the uppercased `name`
                       (e.g. BULBASAUR for Bulbasaur).
    `buffs` (dict) - dictionary mapping Accuracy, Attack, and Defense values
                     for a Pokemon during a battle. Defaults values to 0 each.
    """
    # Constants for Pokemon. A collected Pokemon must have a level between
    # STARTER_LVL and MAX_LVL.
    STARTER_LVL = 5
    MAX_LVL = 100
    # This coefficient is used to calculate stats based on a Pokemon's base hp
    # and its level. Pokemon with higher levels have higher HP/DP stats.
    LVL_COEFFICIENT = 1.1  # hp stats -> (lvl * 1.1) + base hp

    def __init__(self, pid, name, desc, type, weakness, hp, moves):
        """
        Constructs a Pokemon with a given `pid` (int), `name` (str),
        `desc` (str), `type`, (str), `weakness` (str), `hp` (int),
        and `moves` (list of Move objects) using the same initialization
        of a PokemonSpecies. Additionally initializes a `nickname` to
        the uppercased `name` string, `level` to `STARTER_LVL`,
        `curr_hp` to `hp`, and an 3-element dictionary initializing
        "Accuracy", "Attack", and "Defense" buff values to 0. These
        buffs can be increased/decreased as a result of moves played.
        """
        super().__init__(pid, name, desc, type, weakness, hp, moves)
        # Extra attributes specific to unique Pokemon
        self.nickname = self.name.upper()
        self.level = self.STARTER_LVL
        self.curr_hp = hp
        self.buffs = {
            'Accuracy': 0,
            'Attack': 0,
            'Defense': 0
        }

    def __str__(self):
        """
        A method that returns the string representation of a collected Pokemon
        as: <name> "<nickname>" (<type>).
        """
        return f'{self.name} "{self.nickname}" ({self.type})'
    
    def get_stats(self):
        """
        This method takes no arguments and returns a fromat string 
        representation of a Pokemon's stats in the format:
        Lvl <level>, Type: <type>, Weakness: <weakness>

        Arguments: None
        Return Value: a formated str
        """
        return (f'Lvl {self.level}, Type: {self.type},'
            + f' Weakness: {self.weakness}')

    def set_nickname(self, nickname):
        """
        This methods takes a str nickname argument and replaces the 
        current pokemon object's nickname with that nickname.

        Arguments: nickname(str)
        Return Value: None
        """
        self.nickname = nickname
    
    def set_level(self, int_lvl):
        """
        This method takes a level int argument and if the level is valid
        resets the pokemon's current level with the new level argument.

        Arguments: int_lvl(int)
        Return Value: None
        """
        # Unless I turn int_value to an int, it gives me a error saying I 
        #cannot compare str(int_lvl) to an int self.Starter_level.
        if int(int_lvl) < self.STARTER_LVL or int(int_lvl) > self.MAX_LVL:
            print(f'Invalid level {int_lvl}, must be between {self.STARTER_LVL}'
                 + f' and {self.MAX_LVL}')
        else:
            self.level = int_lvl
    
    def level_up(self):
        """
        This method takes not arguments and increments the pokemon's level
        by 1 if it isnt already at Max level and prints the change.

        Arguments: None
        Return Value: None
        """
        if self.level != self.MAX_LVL:
            self.level += 1
            print(f'{self.name} leveled up to level {self.level}!')
        else:
            print(f'{self.name} is already at max level of {self.MAX_LVL}')

