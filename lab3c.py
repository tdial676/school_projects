"""
Thierno Diallo

CS 1 Assignment 3, section C.

Miniproject on L-systems (Lindenmayer systems).

References:
  http://en.wikipedia.org/wiki/L-systems
  http://www.kevs3d.co.uk/dev/lsystems/
"""

import math


# ----------------------------------------------------------------------
# Example L-systems.
# ----------------------------------------------------------------------

# Each L-system consists of two dictionaries:
# 1) a dictionary giving the start state and the transition rules
# 2) a dictionary giving the drawing commands associated with L-system
#    characters


# Koch snowflake.
koch = {'start': 'F++F++F',
        'F': 'F-F++F-F'}
koch_draw = {'F': 'F 1',
             '+': 'R 60',
             '-': 'L 60'}


# Hilbert curve.
hilbert = {'start': 'A',
           'A': '-BF+AFA+FB-',
           'B': '+AF-BFB-FA+'}
hilbert_draw = {'F': 'F 1',
                '-': 'L 90',
                '+': 'R 90'}


# Sierpinski triangle.
sierpinski = {'start': 'F-G-G',
              'F': 'F-G+F+G-F',
              'G': 'GG'}
sierpinski_draw = {'F': 'F 1',
                   'G': 'F 1',
                   '+': 'L 120',
                   '-': 'R 120'}


# ---------------------------------------------------------------------- 
# L-systems functions.
# ---------------------------------------------------------------------- 


def update(lsys, s):
    """
    This function takes a L-system dictionary and an L-system str and returns
    the next version of the L-system str. 

    Argument: 
    - a dictionary containg the starting string of and the rules for an L-system 
    - an L-system str.
    Return Value: a str contaiing the updated version of the L-system str argument.
    """
    if lsys == koch:
        new_str = s.replace('F', lsys['F'])
    elif lsys == hilbert:
        hold_str1 = s.replace('B', 'Z')
        hold_str2 = hold_str1.replace('A', lsys['A'])
        new_str = hold_str2.replace('Z', lsys['B'])
    else:
        hold_str1 = s.replace('G', 'Z')
        hold_str2 = hold_str1.replace('F', lsys['F'])
        new_str = hold_str2.replace('Z', lsys['G'])
    return new_str


def iterate(lsys, n):
    """
    This function function takes an L-system dictionary and an int representing 
    the desired number of iterations of the L-system from it's starting postion 
    and returns the final iteration as a str.

    Argument: 
    - a dictionary containg the starting string of and the rules for an L-system 
    - an int representing the desired number of iterations.
    Return Value: the final iteration of the L-system as a str.
    """
    s = lsys['start']
    for num in range(n):
        s = update(lsys, s)
    return s


def lsystem_to_drawing_commands(draw, s):
    """
    This function takes a dictionary of drawing instructions and an L-system string 
    and returns alist of drawing commands for that L-system.

    Argument: 
    - a dictionary whose keys are characters in L-system strings 
    and whose values are drawing commands
    - an L-system str.
    Return Value: a list of strings containing drawing instructions for that L-system.
    """
    result = []
    for char in s:
        value = draw[char]
        result.append(value)
    return result


def next_location(x, y, angle, cmd):
    """
    This function takes the current x,y position, and angle of the turtle(the pen) and 
    the command it's drawing and returns its new position after executing the commands.

    Arguments: 
    - the x position of the turtle as a float
    - the y position of the turtle as a float
    - the angle of the turtle as an int
    - the command to be executed as a str.
    Return value: a tuple containing the float value of the new x and y position of 
    the turtle. Also, in the tuple is the angle of the turtle as an int.
    """
    move = cmd.split()
    rad_angle = float(angle) * (math.pi / 180)
    if move[0] == 'L':
        angle = (angle + float(move[1])) % 360
    elif move[0] == 'R':
        angle = (angle - float(move[1])) % 360
        if angle < 0:
            while angle < 0:
                angle += 360
    else:
        x += float(move[1]) * math.cos(rad_angle)
        y += float(move[1]) * math.sin(rad_angle)
    return (x, y, angle)


def bounds(cmds):
    """
    This function takes a list of commands and returns the bounding cordinates
    of the resulting drawing as a tuple.

    Arguments: A str list of str commands
    Return Value: a tuple containing the bounding float cordinates of the 
    drawing(xmin, xmax, ymin,ymax)
    """
    x_min = 0.0
    y_min = 0.0
    x_max = 0.0
    y_max = 0.0
    current_location = (0.0,0.0,0.0)
    for cmd in cmds:
        current_location = next_location(current_location[0],
                                         current_location[1],
                                         current_location[2],
                                         cmd)
        if current_location[0] >= x_max:
            x_max = current_location[0]
        elif current_location[0] <= x_min:
            x_min = current_location[0]
        if current_location[1] >= y_max:
            y_max = current_location[1]
        elif current_location[1] <= y_min:
            y_min = current_location[1]
    return (x_min, x_max, y_min, y_max)


def save_drawing(filename, bounds, cmds):
    """
    This function takes a file name str, the bounds of a drawing, and the str 
    list commands for the drawing and writes them to to that file.

    Arguments: 
    - a str file name 
    - a tuple containing float boundaries 
    - a str list of commands
    Return Value: this function has no return value
    """
    file = open(filename, 'w')
    file_info = f'{bounds[0]} {bounds[1]} {bounds[2]} {bounds[3]} \n'
    for cmd in cmds:
        file_info += f'{cmd} \n'
    file.write(file_info)


def make_drawings(name, lsys, ldraw, imin, imax):
    """Make a series of L-system drawings at different iteration levels.

    Arguments:
    - name: the root name of the files to be generated
    - lsys: the L-system dictionary
    - ldraw: the drawing commands for the L-system
    """
    print('Making drawings for {}...'.format(name))
    for i in range(imin, imax):
        s = iterate(lsys, i)
        cmds = lsystem_to_drawing_commands(ldraw, s)
        b = bounds(cmds)
        save_drawing('{}_{}'.format(name, i), b, cmds)


def make_all_drawings():
    """Make a group of drawings of different L-systems.

    The L-systems are simulated at different iteration levels.
    The drawings are saved as files.
    """
    make_drawings('koch', koch, koch_draw, 0, 6)
    make_drawings('hilbert', hilbert, hilbert_draw, 1, 7)
    make_drawings('sierpinski', sierpinski, sierpinski_draw, 0, 7)


if __name__ == '__main__':
    make_all_drawings()
