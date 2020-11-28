import PIL
from cmu_112_graphics import *
import tkinter as tk




# https://stackoverflow.com/questions/47996285/how-to-draw-a-line-following-your-mouse-coordinates-with-tkinter
# ^ how to draw lines in tkinter ???
# if mouse pressed: pen down = true
# if mouse pressed again: pen down = false
# if pen down == True: draw line following mouse's path

def appStarted(app):
    app.penDown = False
    app.coordsList = []

def mousePressed(app, event):
    app.penDown = not app.penDown
    x, y = event.x, event.y
    app.coordsList.append((x, y))

def keyPressed(app, event):
    if (event.key) == 'Space':
        import what

def draw(app, canvas):
    for i in range(len(app.coordsList) - 1):
        x1, y1 = app.coordsList[i]
        x2, y2 = app.coordsList[i+1]
        canvas.create_line(x1, y1, x2, y2)


def redrawAll(app, canvas):
    return


runApp(width=400, height=400)

