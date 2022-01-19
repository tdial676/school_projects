"""
CS 1 21fa
Utility data and functions for use with Rubik's cube program.
"""

import string  # for ascii characters

#
# Utility data.
#

# Built-in user commands.
user_commands = {
    # ----------------------------------------------------------------------
    # Basic moves.
    # ----------------------------------------------------------------------

    # Cube slices.
    "m": "x' l' r",
    "m'": "x  l  r'",
    "e": "y' u  d'",
    "e'": "y  u' d",
    "s": "z  f' b",
    "s'": "z' f  b'",

    # Double moves.
    "u2": "u u",
    "d2": "d d",
    "f2": "f f",
    "b2": "b b",
    "l2": "l l",
    "r2": "r r",

    "m2": "m m",
    "e2": "e e",
    "s2": "s s",

    "x2": "x x",
    "y2": "y y",
    "z2": "z z",

    # ----------------------------------------------------------------------
    # Algorithms.
    # ----------------------------------------------------------------------

    # ------------------------------
    # Top layer.
    # ------------------------------

    # Move edge cube to top layer.
    "df->uf'": "f' u' r u",

    # Move corner cube from top to bottom layer.
    "ufr->dfr": "r' d' r d",
    # Move corner cube from bottom to top layer.
    "dfr->ufr": "f d f'",

    # Orient corner cube in top layer.
    "ufr" : "f d f' d' f d f'",
    "ufr'": "r' d' r d r' d' r",

    # ------------------------------
    # Middle layer.
    # ------------------------------

    "uf->fr": "u r u' r' f r' f' r",
    "uf->lf": "u' l' u l f' l f l'",

    # ------------------------------
    # Last layer.
    # ------------------------------

    # Edge orientation.
    "fur"   : "f u r u' r' f'",
    "fru"   : "f r u r' u' f'",

    # Edge permutation.
    "ep"    : "r u r' u r u2 r' u",

    # Corner orientation.
    "cyc3"  : "r' u l u' r u l' u'",
    "cyc3'" : "u l u' r' u l' u' r",

    # Corner permutation.
    "rd"    : "r d r' d' r d r' d'",
    "dr"    : "d r d' r' d r d' r'",
    "rot2"  : "rd u' dr u",
    "rot2'" : "dr u' rd u",
    "rot2d" : "rd u2 dr u2",
    "rot2d'": "dr u2 rd u2",
    "rot3"  : "rd u' rd u' rd u2",
    "rot3'" : "dr u' dr u' dr u2",
}


# ----------------------------------------------------------------------
# Utility functions.
# ----------------------------------------------------------------------
def move_to_string(face, dir):
    """
    Return the string representation of a quarter-turn move.

    Arguments:
        face (str) - single-character cube face
        dir (str) - direction for the move ('+' or '-')

    Return:
        (str) representation of the move, e.g. "D'"
    """
    assert face in ['U', 'D', 'F', 'B', 'L', 'R', 'X', 'Y', 'Z']
    assert dir in ['+', '-']
    face = face.lower()
    if dir == '+':
        dir = ''
    else:
        dir = "'"  # the ' character
    return face + dir


def adjacent(face1, face2):
    """
    Returns true if two faces are adjacent.

    Arguments:
        face1 (str) - single-character cube face
        face2 (str) - single-character cube face

    Return:
        (bool) True if the two faces are adjacent, otherwise False.
    """
    all_faces = ['U', 'D', 'L', 'R', 'F', 'B']
    assert face1 in all_faces
    assert face2 in all_faces
    non_adjacents = [
        ('U', 'D'), ('D', 'U'),
        ('L', 'R'), ('R', 'L'),
        ('F', 'B'), ('B', 'F')
    ]
    return (face1, face2) not in non_adjacents


def test_faces(size):
    """
    Fill all faces of a size x size x size cube with different characters,
    for testing.

    Argument:
        'size' (int) - cube size (must be 2 or 3).
    """

    assert size in [2, 3]
    # 54 distinct characters is enough for a 3x3x3 cube.
    chars = string.ascii_letters + '@#'
    faces = 'UDFBLR'
    contents = {}
    skip = size * size
    for (i, face) in enumerate(faces):
        start = i * skip
        end = start + skip
        s = chars[start:end]
        face_colors = []
        s1 = 0
        for _ in range(size):
            face_colors.append(list(s[s1:s1+size]))
            s1 += size
        contents[face] = face_colors
    return contents


def display_face(face):
    """
    Return a list of strings representing a single face of a cube.

    Argument:
        face (str) - single-character cube face
    """

    result = []
    for row in face:
        result.append(' '.join(row))
    return result


def concat_faces(face1, face2, sep=' | '):
    """
    Horizontally concatenate two faces, given a separator 'sep'.
    Both faces should have the same length.
    Return the resulting list of strings.

    Arguments:
        face1 (str) - single-character cube face
        face2 (str) - single-character cube face
        sep (str) - separator for concatenation (defaults to ' | ')

    Return:
        (list) concenation of strings as a separated list.
    """

    assert len(face1) == len(face2)
    result = []
    for (i, ch) in enumerate(face1):
        result.append(ch + sep + face2[i])
    return result


def decorate_lines(lines, prefix, suffix):
    """
    Add a prefix and a suffix to each string in a list of strings.
    Return the new list.  The original list is not modified.

    Arguments:
        lines (list) - list of strings (unmodified)
        prefix (str) - prefix string
        suffix (str) - suffix string

    Return:
        (list) new list of strings with given prefix and suffix
    """
    return list(map(lambda l: prefix + l + suffix, lines))


def display(cube, size):
    """
    Return a string which represents a flattened display of a cube in the
    following format:

        U
      L F R
        D
        B

    Arguments:
        cube (RubiksCube)
        size (int) - size of cube

    Return:
        (str) - flattened string representation of cube.
    """

    blank_face = [[' '] * size] * size
    bl = display_face(blank_face)
    # faces for the display (e.g. 'U' for upper)
    u = display_face(cube['U'])
    # down
    d = display_face(cube['D'])
    # left
    l = display_face(cube['L'])
    # right
    r = display_face(cube['R'])
    # forward
    f = display_face(cube['F'])
    # back
    b = display_face(cube['B'])

    # Display the cube like this:
    #
    #     U
    #   L F R
    #     D
    #     B

    # Separator lines.

    n = 2 * size + 1
    spacer = ' ' * (n + 1)
    dashes = '-' * n
    sep1 = ' ' + spacer + '+' + dashes + '+\n'
    sep2 = ' ' + ('+' + dashes) * 3 + '+\n'

    # Put it all together.

    result = '\n'
    result += sep1

    lines1 = concat_faces(bl, concat_faces(u, bl))
    result += ''.join(decorate_lines(lines1, '   ', '\n'))
    result += sep2

    lines2 = concat_faces(l, concat_faces(f, r))
    result += ''.join(decorate_lines(lines2, ' | ', ' |\n'))
    result += sep2

    lines3 = concat_faces(bl, concat_faces(d, bl))
    result += ''.join(decorate_lines(lines3, '   ', '\n'))
    result += sep1

    lines4 = concat_faces(bl, concat_faces(b, bl))
    result += ''.join(decorate_lines(lines4, '   ', '\n'))
    result += sep1

    return result


# Creates some cubes (a 2x2 and 3x3) and displays them.
if __name__ == '__main__':
    cube2 = {
        'U': [['w', 'w'], ['w', 'w']],
        'D': [['y', 'y'], ['y', 'y']],
        'L': [['o', 'o'], ['o', 'o']],
        'R': [['r', 'r'], ['r', 'r']],
        'F': [['g', 'g'], ['g', 'g']],
        'B': [['b', 'b'], ['b', 'b']],
    }

    cube3 = {
        'U': [['w', 'w', 'w'], ['w', 'w', 'w'], ['w', 'w', 'w']],
        'D': [['y', 'y', 'y'], ['y', 'y', 'y'], ['y', 'y', 'y']],
        'L': [['o', 'o', 'o'], ['o', 'o', 'o'], ['o', 'o', 'o']],
        'R': [['r', 'r', 'r'], ['r', 'r', 'r'], ['r', 'r', 'r']],
        'F': [['g', 'g', 'g'], ['g', 'g', 'g'], ['g', 'g', 'g']],
        'B': [['b', 'b', 'b'], ['b', 'b', 'b'], ['b', 'b', 'b']],
    }

    print(display(cube2, 2))
    print(display(cube3, 3))
