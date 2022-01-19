"""
Thierno Diallo
tdiallo@caltech.edu

Rubik's cube representations and basic operations.
"""
import copy
from typing import Sized  # copy for copy.deepcopy
import rubiks_utils as rutils


class RubiksRep:
    """
    Basic functionality of Rubik's cubes.
    """

    def __init__(self, size):
        """
        Initialize the cube representation with non-negative
        size of cube.
        """
        assert size > 0
        face_colors = [
            ('U', 'w'), ('D', 'y'), ('F', 'r'),
            ('B', 'o'), ('L', 'g'), ('R', 'b')
        ]
        self.size = size
        self.face_contents = {}
        for pair in face_colors:
            rows = list(pair[1] * size)
            cell = []
            for num in range(0, size):
                # we append a copy to avoid aliasing or otherwise won't pass.
                cell.append(rows[:])
            self.face_contents[pair[0]] = cell[:]

    def get_row(self, face, row):
        """
        Return a copy of the indicated row on the indicated face.
        The internal representation of the cube is not altered.

        Arguments:
            face (str) - single-character face string.
            row (int) - row between [0, size)

        Return:
            (list)
        """
        assert face in self.face_contents
        assert row >= 0 and row < self.size
        fin_lst = []
        for num in range(0, self.size):
            fin_lst.append(self.face_contents[face][row][num])
        return fin_lst

    def get_col(self, face, col):
        """
        Return a copy of the indicated column on the indicated face.
        The internal representation of the cube is not altered.

        Arguments:
            face (str) - single-character face string.
            col (int) - col between [0, size)

        Return:
            (list) - list of strings
        """
        assert face in self.face_contents
        assert col >= 0 and col < self.size
        fin_lst = []
        for num in range(0, self.size):
            fin_lst.append(self.face_contents[face][num][col])
        return fin_lst

    def set_row(self, face, row, values):
        """
        Change the contents of the indicated row on the indicated face.
        The internal representation of the cube is not altered.
        """
        assert face in self.face_contents
        assert row >= 0 and row < self.size
        assert type(values) is list
        assert len(values) == self.size
        val = values[:]
        self.face_contents[face][row] = val

    def set_col(self, face, col, values):
        """
        Change the contents of the indicated column on the indicated face.
        The internal representation of the cube is not altered.
        """
        assert face in self.face_contents
        assert col >= 0 and col < self.size
        assert type(values) is list
        assert len(values) == self.size
        val = values[:]
        for num in range(0, len(values)):
            self.face_contents[face][num][col] = val[num]

    def get_face(self, face):
        """
        Return the colors of a face, as a list of lists.
        """
        assert face in self.face_contents
        face_lst = []
        for num in range(0, self.size):
            face_lst.append(self.face_contents[face][num])
        return face_lst

    # Basic operations.

    def rotate_face_cw(self, face):
        """
        Rotate a given face clockwise.

        Argument:
            face (str) - single-character face string.
        """
        # There is a shorter way to write this function using get_face(), but
        # the intructions required that we use get_row or get_col
        assert face in self.face_contents
        rows = []
        for num in range(0, self.size):
            rows.append(self.get_row(face, num))
        for num2 in range(0, self.size):
            self.set_col(face, num2, rows[(self.size - (num2 + 1))])

    def rotate_face_ccw(self, face):
        """
        Rotate a given face counterclockwise.

        Argument:
            face (str) - single-character face string.
        """
        assert face in self.face_contents
        for num in range(0, 3):
            self.rotate_face_cw(face)

    def move_front(self):
        """
        Move the F (front) face one-quarter turn clockwise.
        """
        self.rotate_face_cw('F')
        l_col = self.get_col('L', self.size - 1)
        r_col = self.get_col('R', 0)
        u_row = self.get_row('U', self.size - 1)
        d_row = self.get_row('D', 0)
        l_col.reverse()
        self.set_row('U', self.size - 1, l_col)
        r_col.reverse()
        self.set_row('D', 0, r_col)
        self.set_col('R', 0, u_row)
        self.set_col('L', self.size - 1, d_row)

    def rotate_cube_x(self):
        """
        Rotate the cube in the positive X direction.
        """

        up = self.face_contents['U']
        front = self.face_contents['F']
        back = self.face_contents['B']
        down = self.face_contents['D']
        self.face_contents['B'] = up
        self.face_contents['U'] = front
        self.face_contents['D'] = back
        self.face_contents['F'] = down
        self.rotate_face_cw('R')
        self.rotate_face_ccw('L')

    def rotate_cube_y(self):
        """
        Rotate the cube in the positive Y direction.
        """
        front = self.face_contents['F']
        back = self.face_contents['B']
        left = self.face_contents['L']
        right = self.face_contents['R']
        self.face_contents['F'] = right
        self.face_contents['B'] = left
        self.face_contents['L'] = front
        self.face_contents['R'] = back
        self.rotate_face_ccw('D')
        self.rotate_face_cw('U')
        for num in range(0, 2):
            self.rotate_face_cw('R')
            self.rotate_face_cw('B')

    def rotate_cube_z(self):
        """
        Rotate the cube in the positive Z direction.
        """
        down = self.face_contents['D']
        right = self.face_contents['R']
        up = self.face_contents['U']
        left = self.face_contents['L']
        self.face_contents['D'] = right
        self.face_contents['R'] = up
        self.face_contents['U'] = left
        self.face_contents['L'] = down
        self.rotate_face_ccw('B')
        for charecter in 'FLURD':
            self.rotate_face_cw(charecter)

    def display(self):
        """
        Return a string version of the cube representation.
        """

        return rutils.display(self.face_contents, self.size)

    def test_faces(self):
        """
        Load the representation with unique characters. For testing.
        """

        self.face_contents = rutils.test_faces(self.size)


if __name__ == '__main__':
    rep = RubiksRep(3)
    rep.test_faces()
    print(rep.display())
    rep.rotate_cube_z()
    print(rep.display())
