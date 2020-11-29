import tkinter as tk
from cmu_112_graphics import *
'''def myfunction(event):
    x, y = event.x, event.y
    if canvas.old_coords:
        x1, y1 = canvas.old_coords
        canvas.create_line(x, y, x1, y1)
    canvas.old_coords = x, y

def reset_coords(event):
    canvas.old_coords = None

root = tk.Tk()

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()
canvas.old_coords = None


root.bind('<B1-Motion>', myfunction)

root.mainloop()'''

def appStarted(app):
    app.x1 = None
    app.y1 = None
    app.x2 = None
    app.y2 = None
    app.makeLine = []
    app.penDown = False

def mousePressed(app, event): 
    app.penDown = not app.penDown
    x, y = event.x, event.y
    app.makeLine.append((x, y))

def mouseMoved(app, event):
    x, y = event.x, event.y
    app.makeLine.append((x, y))

def drawLine(app, canvas):
    for i in range(len(app.makeLine) - 1):
        if app.makeLine[i + 1] != None:
            x1, y1 = app.makeLine[i]
            x2, y2 = app.makeLine[i + 1]
            canvas.create_line(x1, y1, x2, y2)


def redrawAll(app, canvas):
    if app.penDown:
        drawLine(app, canvas)
    


    

runApp(width=400, height=400)
