"""
Thierno Diallo

Lab5c question 2
"""
from tkinter import *
from math import pi, sin, cos
from lab5a import random_color, random_size

def draw_line(start, end, color):
    """
    This function draws a line using the qrguments given

    Arguments:
        - a tuple (x,y) start coordinate for the line
        - a tuple (x,y) end coordinate for the line
        - a string color for the line
    Return Value: a string handler for the line
    """
    h = c.create_line(start[0], start[1], end[0], end[1], width=3, fill=color)
    return h


def draw_star(r, x, y):
    """
    This function takes the radius and x, y coordinates and draws a lines
    that forms a star with n many points with a default n = 5.

    Arguments:
        - an int x position
        - an int y position
        - an int r radius
    Return Value: None

    """
    point_lst = []
    angel = 2 * pi / n
    for num in range(n):
        pt = ((x + r * cos(angel * num - pi / 2))
             , y + r * sin(angel * num - pi / 2))
        point_lst.append(pt)
    for num in range(n):
        line = draw_line(point_lst[num], point_lst[int((num - (n / 2)) % n)]
                        , color)
        stars.append(line)

def key_handler(event):
    """
    This function takes a tkinter event and binds the 'q', 'c', 'x', '+', '-' 
    keys to quit the program, change the color of the lines being drawn,
    clear the canvas, increase the umber of lines, and decrease the
    number of lines respectively.

    Arguments: tkinter event
    Return Value: None
    """
    global stars
    global color
    global n
    key = event.keysym
    if key == 'q':
        quit()
    elif key == 'c':
        color = random_color()
    elif key == 'x':
        for star in stars:
            c.delete(star)
        stars = []
    elif key == 'minus':
        n -= 2
    elif key == 'plus':
        n += 2
    

def button_handler(event):
    """
    This function draws a star with a random radius each time the 
    event is called.

    Arguments: tkinter event
    Return Valeu: None
    """
    radius = random_size(50, 150)
    draw_star(radius, event.x, event.y)



if __name__ == '__main__':
    # sets up window and canvas
    root = Tk()
    root.geometry('900x900')
    c = Canvas(root, width=900, height= 900)
    c.pack()

    # sets up color, empty stars list, and default star points
    n = 5
    color = random_color()
    stars = []

    # binds events to keys/buttons
    root.bind('<Key>', key_handler)
    c.bind('<Button-1>', button_handler)

    # Starts inifinite event loop
    root.mainloop()

