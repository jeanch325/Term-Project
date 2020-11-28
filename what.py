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

def mousePressed(app, event): 
    app.x1, app.y1 = event.x, event.y

def mouseDragged(app, event):
    app.x2, app.y2 = event.x, event.y

def drawLine(app, canvas):
    canvas.create_line(app.x1, app.y1, app.x2, app.y2)

def redrawAll(app, canvas):
    if app.x1!= None and app.x2!= None:
        drawLine(app, canvas)

runApp(width=400, height=400)
