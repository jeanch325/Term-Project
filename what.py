import tkinter as tk
from cmu_112_graphics import *

def appStarted(app):
    app.makeLine = []
    app.penDown = False

def mousePressed(app, event): 
    app.penDown = not app.penDown
    app.x1, app.y1 = event.x, event.y
    app.makeLine.append((app.x1, app.y1))


def mouseMoved(app, event):
    if app.penDown:
        x, y = event.x, event.y
        app.makeLine.append((x, y))


def drawLine(app, canvas): 
    for i in range(1, len(app.makeLine) - 1):
        if app.makeLine[i + 1] != None:
            x1, y1 = app.makeLine[i]
            x2, y2 = app.makeLine[i + 1]
            canvas.create_line(x1, y1, x2, y2)

def redrawAll(app, canvas):
    drawLine(app, canvas)

runApp(width=400, height=400)
