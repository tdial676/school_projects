"""
Thierno Diallo
tdiallo@caltech.edu

Rubik's cube class to manage a cube state and moves.
"""

import copy    # copy for copy.deepcopy
import random  # random for random.choice
from rubiks_rep import RubiksRep


class InvalidCube(Exception):
    """
    This exception is raised when a cube has been determined to be in
    an invalid configuration.
    """
    pass


class RubiksCube:
    """
    This class implements all Rubik's cube operations.
    """

    def __init__(self, size):
        """
        Initialize the cube representation with a given size.

        Argument:
            - size (int) - dimension of cube (e.g. 3 for 3x3x3)
        """
        # Cube representation.
        self.rep = RubiksRep(size)
        # Number of moves, quarter-turn metric.
        self.count = 0

    def get_state(self):
        """
        Return a copy of the internal state of this object.
        """
        rep = copy.deepcopy(self.rep)
        return (rep, self.count)

    def put_state(self, rep, count):
        """
        Restore a previous state using passed rep and count.
        """
        self.rep = rep
        self.count = count

    # Basic operations.

    def rotate_cube(self, axis, dir):
        """
        Rotate the cube as a whole.
        The X axis means in the direction of an R turn.
        The Y axis means in the direction of a U turn.
        The Z axis means in the direction of an F turn.
        The + direction is clockwise.
        The - direction is counterclockwise.

        Arguments:
          axis (str) - one of ['X', 'Y', 'Z']
          dir  (str) - one of ['+', '-']

        Return value: none
        """
        assert axis in ['X', 'Y', 'Z']
        assert dir in ['+', '-']
        direction = {'+': 1, '-': 3}
        if axis == 'X':
            for num in range(0, direction[dir]):
                self.rep.rotate_cube_x()
        elif axis == 'Y':
            for num in range(0, direction[dir]):
                self.rep.rotate_cube_y()
        elif axis == 'Z':
            for num in range(0, direction[dir]):
                self.rep.rotate_cube_z()

    def move_face(self, face, dir):
        """
        Move the specified face.

        Arguments:
          - face (str): one of ['U', 'D', 'L', 'R', 'F', 'B']
          - dir  (str): '+' for clockwise or '-' for counterclockwise

        Return value: none
        """
        assert face in ['U', 'D', 'F', 'B', 'L', 'R']
        assert dir in ['+', '-']
        dic = {'+': 1, '-': 3}
        if face == 'U':
            self.rotate_cube('X', '-')
            for num in range(0, dic[dir]):
                self.rep.move_front()
            self.rotate_cube('X', '+')
        elif face == 'D':
            self.rotate_cube('X', '+')
            for num in range(0, dic[dir]):
                self.rep.move_front()
            self.rotate_cube('X', '-')
        elif face == 'B':
            self.rotate_cube('X', '-')
            self.rotate_cube('X', '-')
            for num in range(0, dic[dir]):
                self.rep.move_front()
            self.rotate_cube('X', '+')
            self.rotate_cube('X', '+')
        elif face == 'L':
            self.rotate_cube('Y', '-')
            for num in range(0, dic[dir]):
                self.rep.move_front()
            self.rotate_cube('Y', '+')
        elif face == 'R':
            self.rotate_cube('Y', '+')
            for num in range(0, dic[dir]):
                self.rep.move_front()
            self.rotate_cube('Y', '-')
        else:
            for num in range(0, dic[dir]):
                self.rep.move_front()
        self.count += 1

    def random_rotations(self, n):
        """
        Rotate the entire cube randomly 'n' times.

        Arguments:
          n (int) - number of random rotations to make

        Return value: none
        """
        for _ in range(n):
            rot = random.choice('XYZ')
            dir = random.choice('+-')
            self.rotate_cube(rot, dir)

    def random_moves(self, n):
        """
        Make 'n' random moves.

        Arguments:
          n (int) - number of random moves to make

        Return value: none
        """
        for _ in range(0, n):
            face = random.choice('UDFBLR')
            dir = random.choice('+-')
            self.move_face(face, dir)

    def scramble(self, nrots=10, nmoves=50):
        """
        Scramble the cube.

        Arguments:
          nrots  - number of random cube rotations to make
          nmoves - number of random face moves to make

        Return value: none
        """

        self.random_rotations(nrots)
        self.random_moves(nmoves)
        # Reset count before solving begins.
        self.count = 0

    def is_solved(self):
        """
        Return True if the cube is solved.

        If the cube appears solved but is invalid, raise an
        InvalidCube exception with an appropriate error message.
        """

        # Criteria:
        # - all faces must have only one color
        # - all colors are represented
        # - opposite faces: o and r, g and b, w and y
        # - w face adjacent to g and r
        # FIX
        color_lst = []
        apposits_clr = {'o': 'r', 'g': 'b',
                        'w': 'y', 'r': 'o', 'b': 'g', 'y': 'w'}
        apposits_sides = {'F': 'B', 'D': 'U', 'R': 'L'}
        possible_cubes = [
            'wgr', 'wrb', 'wbo', 'wog',
            'goy', 'gyr', 'grw', 'gwo',
            'ygo', 'yob', 'ybr', 'yrg',
            'rwg', 'rgy', 'ryb', 'rbw',
            'bwr', 'bry', 'byo', 'bow',
            'owb', 'oby', 'oyg', 'ogw'
            ]
        for color in self.rep.face_contents:
            face_lst = []
            face = self.rep.get_face(color)
            for row in face:
                for elem in row:
                    if elem not in face_lst:
                        face_lst.append(elem)
            if len(face_lst) != 1:
                return False
            color_lst.append(face_lst[0])
        for color in color_lst:
            if color not in 'wyrogb':
                raise InvalidCube('An invalid color was found on the cube.')
        if len(color_lst) != 6:
            raise InvalidCube('Your cube does not contain all six colors.')
        for side in apposits_sides:
            opp_color = (
            apposits_clr[self.rep.get_face(side)
            [random.randint(0, self.rep.size - 1)]
            [random.randint(0, self.rep.size - 1)]]
            )
            face_color = (
            self.rep.get_face(apposits_sides[side])
            [random.randint(0, self.rep.size - 1)]
            [random.randint(0, self.rep.size - 1)]
            )
            if opp_color != face_color:
                raise InvalidCube('Not all opposite sides have their ' +
                'supposed opposite color.')
        cubie = (self.rep.get_face('U')[-1][-1] + self.rep.get_face('F')[0][-1]
                + self.rep.get_face('R')[0][0])
        if cubie not in possible_cubes:
            raise InvalidCube('The cube is a mirror image of' +
                              ' what it should be.')
        return True

    def display(self):
        """
        Return a string version of the cube representation.
        """

        return self.rep.display()


if __name__ == '__main__':
    cube = RubiksCube(3)
    print(cube.display())
    cube.scramble()
    print(cube.display())
