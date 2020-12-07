from PIL import Image, ImageDraw, ImageColor
import time
import tkinter as tk 
from cmu_112_graphics import *

def appStarted(mode):
    mode.bluex = mode.width/2
    mode.purplex = mode.bluex - mode.width
    mode.pinkx = mode.purplex - mode.width

    mode.switchLevels = False

def switchBackgrounds(mode):
    if mode.bluex == 1.5 * mode.width:
        mode.bluex = mode.pinkx - mode.width
        mode.switchLevels = False
    if mode.purplex == 1.5 * mode.width:
        mode.purplex = mode.bluex - mode.width
        mode.switchLevels = False
    if mode.pinkx == 1.5 * mode.width:
        mode.pinkx = mode.purplex - mode.width
        mode.switchLevels = False

def sideScroll(mode):
    mode.bluex += 20
    mode.purplex += 20
    mode.pinkx += 20
    mode.switchBackgrounds()

def timerFired(mode):
    if mode.switchLevels:
        mode.sideScroll()


def keyPressed(mode, event):
    if event.key == 'Space':
        mode.switchLevels = True
    

def redrawAll(mode, canvas):
    blue = PhotoImage(file='blue.png')
    canvas.create_image(mode.bluex, mode.height/2, image=blue)

    purple = PhotoImage(file='purple.png')
    canvas.create_image(mode.purplex, mode.height/2, image=purple)

    pink = PhotoImage(file='pink.png')
    canvas.create_image(mode.pinkx, mode.height/2, image=pink)
    
    
runApp(width=500, height=500)