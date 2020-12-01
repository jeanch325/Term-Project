from cmu_112_graphics import *
import random
import time


# mode class structure is from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#subclassingModalApp

class SplashScreenMode(Mode):
    def redrawAll(mode, canvas):
        font = 'Arial 20 bold'
        canvas.create_text(mode.width/2, mode.height/2, 
                        text='welcome page\nclick enter to begin', 
                        font='Arial 20 bold')

    def keyPressed(mode, event):
        if event.key == 'Enter':
            mode.app.setActiveMode(mode.app.helpMode)

class DrawingMode(Mode):
    def appStarted(mode):
        mode.xMargin = 50
        mode.topMargin = 75
        mode.bottomMargin = 25
        mode.cols = 25
        mode.rows = 25
        mode.selection = (-1, -1) # (row, col) of selection, (-1,-1) for none
        mode.color = 'black'
    
    # grid code from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
    def pointInGrid(mode, x, y):
        # return True if (x, y) is inside the grid defined by app.
        return ((mode.xMargin <= x <= mode.width-mode.xMargin) and
                (mode.bottomMargin <= y <= mode.height-mode.topMargin))

    def getCell(mode, x, y):
        # aka "viewToModel"
        # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        if (not mode.pointInGrid(x, y)):
            return (-1, -1)
        gridWidth  = mode.width - 2*mode.xMargin
        gridHeight = mode.height - mode.topMargin - mode.bottomMargin
        cellWidth  = gridWidth / mode.cols
        cellHeight = gridHeight / mode.rows

        # Note: we have to use int() here and not just // because
        # row and col cannot be floats and if any of x, y, mode.margin,
        # cellWidth or cellHeight are floats, // would still produce floats.
        row = int((y - mode.bottomMargin) / cellHeight)
        col = int((x - mode.xMargin) / cellWidth)

        return (row, col)

    def getCellBounds(mode, row, col):
        # aka "modelToView"
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        gridWidth  = mode.width - 2*mode.xMargin
        gridHeight = mode.height - mode.topMargin - mode.bottomMargin
        cellWidth = gridWidth / mode.cols
        cellHeight = gridHeight / mode.rows
        x0 = mode.xMargin + col * cellWidth
        x1 = mode.xMargin + (col+1) * cellWidth
        y0 = mode.topMargin + row * cellHeight
        y1 = mode.bottomMargin + (row+2) * cellHeight
        return (x0, y0, x1, y1)

    def mousePressed(mode, event):
        (row, col) = mode.getCell(event.x, event.y)
        # select this (row, col) unless it is selected
        if (mode.selection == (row, col)):
            mode.selection = (-1, -1)
        else:
            mode.selection = (row-2, col)

    def redrawAll(mode, canvas):
        font = 'Arial 20 bold'
        drawing = 'Drawing'
        canvas.create_text(10, 10, text=drawing, 
                                font='Arial 20 bold', anchor=NW)
        click = '1. click "s" to save character\n2. click enter to begin game\n'
        canvas.create_text(mode.width - 10, 10, 
                        text=click, font='Arial 15', anchor=NE)

        for row in range(mode.rows):
            for col in range(mode.cols):
                (x0, y0, x1, y1) = mode.getCellBounds(row, col)
                if (mode.selection == (row, col)):
                    fill = mode.color  
                else:
                    fill = 'white'
                canvas.create_rectangle(x0, y0, x1, y1, fill=fill, width=1)

    def keyPressed(mode, event):
        if event.key == 'h':
            mode.app.setActiveMode(mode.app.helpMode)
        elif event.key == 'Enter':
            mode.app.setActiveMode(mode.app.gameMode)
        elif event.key == 's':
            # save and uplad image
            pass


class GameMode(Mode):
    def appStarted(mode):
        mode.penDown = False

        mode.makeLine = []
        mode.newLevel = True

        mode.mouseMovedDelay = 0

        mode.chickenx = 5
        mode.chickeny = 5
        mode.chickenSize = 50
        mode.direction = 'right'
        mode.dx = 7
        mode.dy = 15 

        mode.go = False
        mode.onSurface = False

        mode.i = 0

        mode.sBlockW = 100
        mode.sBlockH = 74
        mode.lBlockW = 200
        mode.sBlockH = 74
        mode.level = 1
        mode.blocks = []
        



    def keyPressed(mode, event):
        if event.key == 'h':
            mode.penDown = False
            mode.app.setActiveMode(mode.app.helpMode)
        elif not mode.go and event.key == 'd':
            mode.app.setActiveMode(mode.app.drawingMode)
        elif event.key == 'r':
            mode.makeLine.clear()
            
    def mousePressed(mode, event): 
        if mode.newLevel:
            mode.go = True
            mode.penDown = not mode.penDown
            if mode.penDown:
                x1, y1 = event.x, event.y
                mode.makeLine.append((x1, y1))
            if not mode.penDown and len(mode.makeLine) != 0:
                mode.newLevel = False

    def mouseMoved(mode, event):
        if mode.penDown:
            x, y = event.x, event.y
            mode.makeLine.append((x, y))

    def setUpBlocks(mode, blockW, blockH, level):
        for i in range(level):
            x0 = random.randrange(mode.width-blockW)
            y0 = random.randrange(mode.height-blockH)
            x1 = x0 + blockW
            y1 = y0 + blockH
            newBlock = (x0, y0, x1, y1)
            mode.blocks.append(newBlock)
            for oldBlock in mode.blocks:
                xRange = oldBlock[2] - oldBlock[0] 
                yRange = oldBlock[3] - oldBlock[1]
                if ((x0 in range(xRange) or x1 in range(xRange)) and
                    y0 in range(yRange) or y1 in range(yRange)):
                    mode.blocks.remove(newBlock)


    def makeBlocks(mode):
        # small Blocks:
        setUpBlocks(mode.sBlockW, mode.sBlockH, mode.level)
        # small Blocks:
        setUpBlocks(mode.lBlockW, mode.lBlockH, mode.level)

        # draw blocks
        



    def checkSurface(mode, surfaceList, chickenCent, chickenr, chickenPath):
        # helper for move(mode, chickenPath)
        for point in surfaceList:
            x, y = point
            # checking if chicken's position is above and in x, y range of surface
            if abs(y - (mode.chickeny + chickenr)) <= (chickenr + mode.dy): 
                if abs(x - (mode.chickenx + chickenr)) <= (chickenr + mode.dx):
                    mode.onSurface = True
                    chickenPath.append((x, y))
                    
        

    def move(mode, chickenPath, i):
        # moves chicken left, right, and down
        chickenCent = mode.chickenx + (0.5 * mode.chickenSize)
        chickenr = mode.chickenSize // 2
        chickenPath = []

        # check for line: if valid, it adds a point
        mode.checkSurface(mode.makeLine, chickenCent, chickenr, chickenPath) 
        if mode.onSurface:
            x, y = chickenPath[i]

            mode.chickenx = (x + mode.chickenSize)
            mode.chickeny = (y - mode.chickenSize)
            time.sleep(0.05) # from https://stackoverflow.com/questions/16555120/how-can-i-slow-down-a-loop-in-python
            if i + 1 == len(chickenPath):
                mode.onSurface = False
                i = 0

        

    def moveChicken(mode, i):
        chickenPath = []
        mode.move(chickenPath, i)


    def timerFired(mode):
        if mode.go:
            mode.moveChicken(mode.i) 
            mode.i += 1
            mode.chickeny += mode.dy
            if (mode.chickeny + mode.chickenSize) >= mode.height:
                mode.chickeny = mode.height - mode.chickenSize
            if (mode.onSurface == False):
                mode.chickenx += mode.dx 
                if (mode.chickenx < 0) or ((mode.chickenx + mode.chickenSize)> mode.width): 
                    mode.dx = -mode.dx



    def redrawAll(mode, canvas):
        for i in range(1, len(mode.makeLine) - 1):
            if mode.makeLine[i + 1] != None:
                x1, y1 = mode.makeLine[i]
                x2, y2 = mode.makeLine[i + 1]
                canvas.create_line(x1, y1, x2, y2, width=7)
        chicken = PhotoImage(file='chicken.png')
        canvas.create_image(mode.chickenx, mode.chickeny, image=chicken, anchor=NW)

        # why doesn't this work
        for block in mode.blocks:
            (x0, y0, x1, y1) = block
            shortBlock = PhotoImage(file='short-block.png')
            canvas.create_image(x0, y0, image=shortBlock)

class HelpMode(Mode):
    def redrawAll(mode, canvas):
        loc = mode.height/2 - 140
        canvas.create_rectangle(mode.width/2 - 120, mode.height/2 - 120, 
                                mode.width/2 + 160, mode.height/2 + 160, fill='blue')
        canvas.create_rectangle(mode.width/2 - 140, mode.height/2 - 140, 
                                mode.width/2 + 140, mode.height/2 + 140, fill='white')

        canvas.create_text(mode.width/2, loc + 20, text='HELP PAGE', font='Arial 20 bold') 
        canvas.create_text(mode.width/2, loc + 50, text='* press r to restart') 
        canvas.create_text(mode.width/2, loc + 80, text='* press h to access/leave help page')
        canvas.create_text(mode.width/2, loc + 110, text='* press d to access/leave drawing page')
        canvas.create_text(mode.width/2, loc + 140, text='* press h to access/leave help page')
        canvas.create_text(mode.width/2, loc + 170, text='* click once to put pen down') 
        canvas.create_text(mode.width/2, loc + 190, text='and move mouse to draw.') 
        canvas.create_text(mode.width/2, loc + 220, text='* click again to lift pen up') 
        canvas.create_text(mode.width/2, loc + 240, text='and stop drawing.') 
        canvas.create_text(mode.width/2, loc + 270, text='* you have 1 pen per level!') 

    def keyPressed(mode, event):
        if event.key == 'h':
            mode.app.setActiveMode(mode.app.gameMode)
        if event.key == 'd':
            mode.app.setActiveMode(mode.app.drawingMode)

class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        app.helpMode = HelpMode()
        app.setActiveMode(app.splashScreenMode)
        app.drawingMode = DrawingMode()

app = MyModalApp(width=500, height=500)