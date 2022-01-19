"""
Thierno Diallo

Lab5c question 1
"""
from tkinter import *
import random
from lab5a import random_color

def key_handler(event):
    """
    This function takes a tkinter event binds the 'q', 'c', 'x' keys
    to quit the program, change the color of the circles being drawn, 
    and clear the canvas respectively.

    Arguments: tkinter event
    Retturn Value: None
    """
    global circles
    global color
    key = event.keysym
    if key == 'q':
        quit()
    elif key == 'c':
        color = random_color()
    elif key == 'x':
        for circle in circles:
            c.delete(circle)
        circles = []
    

def button_handler(event):
    """
    This function takes a tkinter event, draws a circle, and appends 
    that circle to a list of circles.

    Arguments: tkinter event
    Return Value: None
    """
    radius = (random.randint(10, 50)) / 2
    x1, y1 = (event.x - radius), (event.y - radius)
    x2, y2 = (event.x + radius), (event.y + radius)
    circle = c.create_oval(x1, y1, x2, y2, fill=color, outline=color)
    circles.append(circle)


if __name__ == '__main__':
    #sets up window and canvas
    root = Tk()
    root.geometry('900x900')
    c = Canvas(root, width=900, height= 900)
    c.pack()
    #sets up global initial color and circle list
    color = random_color()
    circles = []

    #binds events to keys/buttons
    root.bind('<Key>', key_handler)
    c.bind('<Button-1>', button_handler)
    
    # Starts inifinite event loop
    root.mainloop()

    