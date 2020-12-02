from cmu_112_graphics import *
import random
import time


# mode class structure is from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#subclassingModalApp

class SplashScreenMode(Mode):
    def redrawAll(mode, canvas):
        font = 'Arial 20 bold'
        canvas.create_text(mode.width/2, mode.height/2, 
                        text='welcome page\nclick enter to begin playing', 
                        font='Arial 20 bold')

    def keyPressed(mode, event):
        if event.key == 'Enter':
            mode.app.setActiveMode(mode.app.gameMode)

class DrawingMode(Mode):
    def appStarted(mode):
        mode.margin = 100
        mode.cols = 25
        mode.rows = 25
        mode.selection = (-1, -1) # (row, col) of selection, (-1,-1) for none
        mode.color = 'black'
        mode.penDown = False
        mode.draw = []
        mode.mouseMovedDelay = 0
        mode.penType = 'pen'
        mode.colors = [['red3', 'red', 'tomato'], 
                        ['dark orange', 'orange', 'gold'], 
                        ['yellow', 'goldenrod3', 'olive drab'], 
                        ['dark green', 'lime green','green'], 
                        ['aquamarine2', 'SteelBlue1', 'dodger blue'], 
                        ['blue', 'medium blue', 'navy'], 
                        ['SlateBlue3', 'purple3',  'purple'], 
                        ['DarkOrchid3', 'magenta2', 'VioletRed2'], 
                        ['maroon1', 'PaleVioletRed1', 'hot pink'], 
                        ['black', 'gray23','gray62'], 
                        ['gray85', 'white', 'saddlebrown'], 
                        ['sienna4', 'sienna1', 'navajo white']]


    # grid code from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids

    def getCell(mode, x, y):
        # aka "viewToModel"
        # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        if (not mode.pointInGrid(x, y)):
            return (-1, -1)
        gridWidth  = mode.width - mode.margin
        gridHeight = mode.height - mode.margin 
        cellWidth  = gridWidth / mode.cols
        cellHeight = gridHeight / mode.rows

        # Note: we have to use int() here and not just // because
        # row and col cannot be floats and if any of x, y, mode.margin,
        # cellWidth or cellHeight are floats, // would still produce floats.
        row = int((y - mode.margin) / cellHeight)
        col = int((x - mode.margin) / cellWidth)

        return (row, col)

    def getCellBounds(mode, row, col):
        # aka "modelToView"
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        gridWidth  = mode.width - mode.margin
        gridHeight = mode.height - mode.margin 
        cellWidth = gridWidth / mode.cols
        cellHeight = gridHeight / mode.rows
        x0 = mode.margin + col * cellWidth
        x1 = mode.margin + (col+1) * cellWidth
        y0 = mode.margin + row * cellHeight
        y1 = mode.margin + (row+1) * cellHeight
        return (x0, y0, x1, y1)
    
    def getColorCellBounds(mode, r, c):
        # aka "modelToView"
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        gridWidth  = mode.margin
        gridHeight = 400
        cellWidth = gridWidth / len(mode.colors[0])
        cellHeight = gridHeight / len(mode.colors)
        x0 = c * cellWidth
        x1 = (c+1) * cellWidth
        y0 = mode.margin + r * cellHeight
        y1 = mode.margin + (r+1) * cellHeight
        return (x0, y0, x1, y1)

    def mousePressed(mode, event): 
        x1, y1 = event.x, event.y
        if (0 < x1 < 100) and (y1 > 100):
             row = (y1 - 100) // 33
             col = x1 // 33
             mode.color = mode.colors[row][col]
        else:
            mode.penDown = not mode.penDown
            if mode.penDown:
                if mode.penType == 'pen':
                    mode.draw.append((x1, y1, mode.color))
                elif mode.penType == 'eraser':
                    # find the cell that the x,y coord is in and remove it but HOW
                    for point in mode.draw:
                        x, y, color = point
                        if (abs(x1-x) < 16) and (abs(y1-y) < 16):
                            mode.draw.remove(point)

    def mouseMoved(mode, event):
        if mode.penDown:
            x1, y1 = event.x, event.y
            if mode.penType == 'pen':
                mode.draw.append((x1, y1, mode.color))
            elif mode.penType == 'eraser':
                for point in mode.draw:
                    x, y, color = point
                    if (abs(x1-x) < 16) and (abs(y1-y) < 16):
                        mode.draw.remove(point)

    def checkPoint(mode, x, y, x0, y0, x1, y1):
        sizex = abs(x0 - x1)
        sizey = abs(y0 - y1)
        if (abs(x0 - x) < sizex and abs(x1 - x) < sizex and abs(y0 - y) < sizey and abs(y1 - y) < sizey): 
            return True



    def redrawAll(mode, canvas):
        # drawing logo
        drawing = PhotoImage(file='drawing.png')
        canvas.create_image(0, 0, image=drawing, anchor=NW)

        # instructions
        canvas.create_rectangle(100, 0, mode.width, 100, fill='black')
        canvas.create_rectangle(105, 7, mode.width-8, 95, fill='white')
        canvas.create_text(120, 10, text='press "e" for eraser', font='Arial 15', anchor=NW)
        canvas.create_text(120, 30, text='pick colors on left', font='Arial 15', anchor=NW)
        canvas.create_text(120, 50, text='press "s" to save', font='Arial 15', anchor=NW)
        canvas.create_text(120, 70, text='press "enter" to play', font='Arial 15', anchor=NW)
        canvas.create_text(290, 10, text='click once to place pen down,', font='Arial 15', anchor=NW)
        canvas.create_text(290, 30, text='click again to lift pen up', font='Arial 15', anchor=NW)

        # color picker            
        for r in range(len(mode.colors)):
            for c in range(len(mode.colors[0])):
                (x0, y0, x1, y1) = mode.getColorCellBounds(r, c)
                canvas.create_rectangle(x0, y0, x1, y1, fill=mode.colors[r][c], width=1)

        # drawing grid
        for row in range(mode.rows):
            for col in range(mode.cols):
                (x0, y0, x1, y1) = mode.getCellBounds(row, col)
                for point in mode.draw:
                    x, y, color = point
                    if mode.checkPoint(x, y, x0, y0, x1, y1):
                        canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=0)
                

    def keyPressed(mode, event):
        if event.key == 'h':
            mode.app.setActiveMode(mode.app.helpMode)
        elif event.key == 'Enter':
            mode.app.setActiveMode(mode.app.gameMode)
        elif event.key == 's':
            mode.app.gameMode.chicken = 'newcharacter.png'
        elif event.key == 'e':
            mode.penType = 'eraser'
        elif event.key == 'p':
            mode.penType = 'pen'
        


class GameMode(Mode):
    def appStarted(mode):
        mode.penDown = False

        mode.makeLine = []
        mode.newLevel = True

        mode.mouseMovedDelay = 0

        mode.chicken = 'chicken.png'
        mode.chickenx = 5
        mode.chickeny = 5
        mode.chickenSize = 50
        mode.direction = 'right'
        mode.dx = 7
        mode.dy = 5 

        mode.go = False
        mode.onSurface = False

        mode.i = 0

        mode.sBlockW = 100
        mode.sBlockH = 74
        mode.lBlockW = 200
        mode.sBlockH = 74
        mode.level = 1
        mode.blocks = []

        mode.chickenPath = []
        



    def keyPressed(mode, event):
        if event.key == 'h':
            mode.penDown = False
            mode.app.setActiveMode(mode.app.helpMode)
        elif event.key == 'r':
            mode.makeLine.clear()
            mode.newLevel = True
            mode.go = False
            mode.chickenx = 5
            mode.chickeny = 5
            
    def mousePressed(mode, event):
        if ((mode.width-110) < event.x < (mode.width-10) and
            10 < event.y < 110):
            mode.app.setActiveMode(mode.app.drawingMode)

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
        # long Blocks:
        setUpBlocks(mode.lBlockW, mode.lBlockH, mode.level)

        # draw blocks
    
    def checkSurface(mode, surfaceList, chickenr):
        # helper for move(mode, chickenPath)
        for point in surfaceList:
            x, y = point
            # checking if chicken's position is above and in x, y range of surface
            if abs(y - (mode.chickeny + chickenr)) <= (mode.chickenSize + mode.dy): 
                if abs(x - (mode.chickenx + chickenr)) <= (mode.chickenSize + mode.dx):
                   mode.chickenPath.append((x, y))
        if len(mode.chickenPath) != 0:
            mode.onSurface = True
        return mode.chickenPath

    def recursive(mode, chickenPath):
        if len(chickenPath) == 0:
            mode.onSurface = False
            mode.chickenx += mode.dx
            return
        else:
            mode.chickenx =  chickenPath[0][0]
            mode.chickeny = (chickenPath[0][1] - mode.chickenSize)
            time.sleep = (0.5)
            return mode.recursive(chickenPath[1:])

    def timerFired(mode): #non recursive
        #print(mode.chickenPath)
        chickenr = mode.chickenSize // 2
        if mode.go:
            if len(mode.chickenPath) == 0 and mode.onSurface == False:
                mode.chickenPath = mode.checkSurface(mode.makeLine, chickenr)
                # call for s blocks and l blocks
            if mode.onSurface:
                if len(mode.chickenPath) == 0:
                    mode.onSurface = False
                    mode.chickenx += mode.dx
                else:
                    mode.chickenx =  mode.chickenPath[0][0]
       	            mode.chickeny = (mode.chickenPath[0][1] - mode.chickenSize)
                    mode.chickenPath.pop(0)

            else:
                mode.chickeny += mode.dy
                if (mode.chickeny + mode.chickenSize) >= mode.height:
                    mode.chickeny = mode.height - mode.chickenSize
                    mode.chickenx += mode.dx
                if (mode.chickenx < 0) or ((mode.chickenx + mode.chickenSize) > mode.width):
                    mode.dx = -mode.dx

    '''def timerFired(mode): # recursive
        chickenr = mode.chickenSize // 2
        if mode.go:
            mode.chickenPath = mode.checkSurface(mode.makeLine, chickenr)
            # call for s blocks and l blocks
            if mode.onSurface:
                mode.recursive(mode.chickenPath)
                mode.onSurface = False
            else:
                mode.chickeny += mode.dy
                
                if (mode.chickeny + mode.chickenSize) >= mode.height:
                    mode.chickeny = mode.height - mode.chickenSize
                    mode.chickenx += mode.dx
                if (mode.chickenx < 0) or ((mode.chickenx + mode.chickenSize) > mode.width):
                    mode.dx = -mode.dx'''


    def redrawAll(mode, canvas):
        # drawing mode button
        drawing = PhotoImage(file='drawing.png')
        canvas.create_image(mode.width-10, 10, image=drawing, anchor=NE)

        for i in range(1, len(mode.makeLine) - 1):
            if mode.makeLine[i + 1] != None:
                x1, y1 = mode.makeLine[i]
                x2, y2 = mode.makeLine[i + 1]
                canvas.create_line(x1, y1, x2, y2, width=7)
        char = PhotoImage(file=mode.chicken)
        canvas.create_image(mode.chickenx, mode.chickeny, image=char, anchor=NW)
        
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

def main():
    app = MyModalApp(width=500, height=500)

if __name__ == '__main__':
    main()