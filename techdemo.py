from tkinter import *
from PIL import Image, ImageDraw, ImageColor
from cmu_112_graphics import *


def getCell(x, y):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    gridWidth  = 25 
    gridHeight = 25
    cellWidth  = gridWidth / mode.cols
    cellHeight = gridHeight / mode.rows

    # Note: we have to use int() here and not just // because
    # row and col cannot be floats and if any of x, y, ,
    # cellWidth or cellHeight are floats, // would still produce floats.
    row = int((y) / cellHeight)
    col = int((x) / cellWidth)

    return (row, col)

def getCellBounds(row, col):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = 100 
    gridHeight = 100
    cellWidth = gridWidth / 25
    cellHeight = gridHeight / 25
    x0 = col * cellWidth
    x1 = (col+1) * cellWidth
    y0 = row * cellHeight
    y1 = (row+1) * cellHeight
    return (x0, y0, x1, y1)

draw = [(10, 20, 'blue'), (15, 25, 'gold'), (20, 30, 'red'), (25, 35, 'green'), (30, 40, 'black')]

for row in range(25):
    for col in range(25):
        (x0, y0, x1, y1) = getCellBounds(row, col)
        for point in draw:
            x, y, color = point
            rgbColor = ImageColor.getrgb(color)
            ImageDraw.polygon([(x0, y0), (x1, y1)], fill=rgbColor, outline=None)



