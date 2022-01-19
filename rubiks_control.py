"""
Thierno Diallo
tdiallo@caltech.edu

Rubik's cube controller (interactive interface).
"""

import copy  # copy for copy.deepcopy
from rubiks_cube import RubiksCube
import rubiks_utils  # for rubiks_utils.user_commands


class InvalidCommand(Exception):
    """
    This exception is raised when an invalid cube command is received.
    """
    pass


class RubiksControl:
    """
    This class implements an interactive Rubik's cube puzzle.
    """

    def __init__(self, size, scramble=True):
        """
        Initialize the cube representation.
        Initialize the set of basic commands.

        Arguments:
            size (int) - the size of the cube (must be 2 or 3)
                         2 means a 2x2x2 cube; 3 means a 3x3x3 cube
            scramble (bool) - True if you want the cube scrambled
        """
        if size not in [2, 3]:
            raise ValueError('Size must be 2 or 3.')
        self.cube = RubiksCube(size)
        self.history = []
        if scramble:
            self.cube.scramble()

        # Built-in commands.
        # Use lower-case for ease of typing.
        # Use double quotes since some commands use the single quote character.
        self.face_moves = \
            ["u", "u'", "d", "d'", "f", "f'",
             "b", "b'", "l", "l'", "r", "r'"]
        self.rotations = ["x", "x'", "y", "y'", "z", "z'"]
        # Deep-copy so util commands aren't modified.
        self.user_commands = copy.deepcopy(rubiks_utils.user_commands)

    def save_commands(self, filename):
        """Save user commands to a file given filename (str)."""
        with open(filename, 'w') as outfile:
            for (cmd, contents) in self.user_commands.items():
                print(f'{cmd} {contents}', file=outfile)

    def exec_load_commands(self, filename):
        """Load user commands from a file given filename (str)."""
        self.user_commands = {}
        with open(filename) as infile:
            for line in infile:
                words = line.split()
                assert len(words) >= 2
                cmd = words[0]
                contents = ' '.join(words[1:])
                self.user_commands[cmd] = contents

    def exec_print_commands(self):
        """
        Print user commands to the terminal, each command
        printed in the format:
        <cmd> : <cmd contents>.
        """
        for (cmd, contents) in self.user_commands.items():
            print(f'{cmd} : {contents}')

    def exec_add_command(self, name, cmds):
        """
        Add a user command. Raises TypeError if name isn't str
        or cmds isn't list.

        Arguments:
          name (str) - the name of the command to add.
          cmds (list) - a list of the command strings that the name should
          expand to.

        Return value: none
        """
        assert type(name) is str
        assert type(cmds) is list
        self.user_commands[name] = ' '.join(cmds)

    def exec_command(self, cmd):
        """
        Execute a command.

        Arguments:
          cmd (str) - a command string to execute

        Return value: none
        """
        assert type(cmd) is str
        if cmd in self.face_moves:
            cmd = cmd.upper()
            if len(cmd) != 1:
                self.cube.move_face(cmd[0], '-')
            else:
                self.cube.move_face(cmd, '+')
        elif cmd in self.rotations:
            cmd = cmd.upper()
            if len(cmd) != 1:
                self.cube.rotate_cube(cmd[0], '-')
            else:
                self.cube.rotate_cube(cmd, '+')
        elif cmd in self.user_commands:
            commands = self.user_commands[cmd].split()
            for elem in commands:
                self.exec_command(elem)
        else:
            raise InvalidCommand(f'The command, {cmd}, is an invalid move.')


    def undo_command(self):
        """
        Undo the last move(s), restoring the previous state.
        """
        if self.history == []:
            raise InvalidCommand('No moves to undo!')
        (rep, count) = self.history.pop()
        self.cube.put_state(rep, count)

    def play(self, check_solved=True):
        """Interactively solve Rubik's cube."""

        while True:
            print(self.cube.display())
            print(f'Move count: {self.cube.count}\n')

            if check_solved and self.cube.is_solved():
                print('SOLVED!')
                break

            cmd = input('cube> ')
            cmds = cmd.split()
            if len(cmds) < 1:
                continue

            try:
                # Quit game.
                if cmds[0] in ['q', 'quit']:
                    break

                # Undo a move.
                if len(cmds) == 1 and cmds[0] in ['-', 'undo']:
                    self.undo_command()

                # Save the commands to a file.
                elif len(cmds) == 2 and cmds[0] == 'save':
                    self.save_commands(cmds[1])

                # Load commands from a file.
                elif len(cmds) == 2 and cmds[0] == 'load':
                    self.exec_load_commands(cmds[1])

                # Print all commands.
                elif len(cmds) == 1 and cmds[0] == 'cmds':
                    self.exec_print_commands()

                # Add a new command if the second word is ':'.
                elif len(cmds) > 2 and cmds[1] == ':':
                    self.exec_add_command(cmds[0], cmds[2:])

                else:
                    # Save the cube state before moving.
                    self.history.append(self.cube.get_state())

                    for subcmd in cmds:
                        self.exec_command(subcmd)

            except InvalidCommand as err:
                print(f'Invalid command line: {cmd}')
                print(err)


if __name__ == '__main__':
    # Leave 'scramble' as True normally.
    # Make it False if you want to test rotations on a solved cube.
    scramble = True
    check_solved = scramble
    cube = RubiksControl(3, scramble)
    cube.play(check_solved)
