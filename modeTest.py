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
        mode.sprite = set()
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

    def keyPressed(mode, event):
        if event.key == 'h':
            mode.app.setActiveMode(mode.app.helpMode)
        elif event.key == 'Enter':
            mode.app.setActiveMode(mode.app.gameMode)
        elif event.key == 's':
            mode.exportSprite()
            mode.app.gameMode.s = mode.sprite
            #mode.app.gameMode.chicken = 'newcharacter.png'
        elif event.key == 'e':
            mode.penType = 'eraser'
        elif event.key == 'p':
            mode.penType = 'pen'

    def checkPoint(mode, x, y, x0, y0, x1, y1):
        sizex = abs(x0 - x1)
        sizey = abs(y0 - y1)
        if (abs(x0 - x) < sizex and abs(x1 - x) < sizex and abs(y0 - y) < sizey and abs(y1 - y) < sizey): 
            return True

    def exportSprite(mode):
        for row in range(mode.rows):
            for col in range(mode.cols):
                (x0, y0, x1, y1) = mode.getCellBounds(row, col)
                for point in mode.draw:
                    x, y, color = point
                    if mode.checkPoint(x, y, x0, y0, x1, y1):
                        mode.sprite.add((row, col, color))

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
                



class GameMode(Mode):
    def appStarted(mode):
        mode.penDown = False

        mode.makeLine = []
        mode.newLevel = True

        mode.mouseMovedDelay = 0

        mode.chicken = 'chicken.png'
        mode.s = set()
        mode.chickenx = 50
        mode.chickeny = 50
        mode.chickenSize = 50
        mode.chickenr = 25
        mode.dx = 7
        mode.dy = 20

        mode.go = False

        mode.i = 0

        mode.timerDelay = 50

        mode.onLine = False

        mode.currentBlockIndex = 0
        mode.sBlockW = 100
        mode.sBlockH = 74
        mode.lBlockW = 200
        mode.lBlockH = 74
        mode.level = 1
        mode.blocks = []

        mode.onBlock = False
        mode.chickenPath = []
        

        mode.makeBlocks()

    def keyPressed(mode, event):
        if event.key == 'h':
            mode.penDown = False
            mode.app.setActiveMode(mode.app.helpMode)
        elif event.key == 'r':
            mode.makeLine.clear()
            mode.newLevel = True
            mode.go = False
            mode.chickenx = 50
            mode.chickeny = 50
            
    def mousePressed(mode, event):
        if ((mode.width-110) < event.x < (mode.width-10) and
            10 < event.y < 110):
            mode.app.setActiveMode(mode.app.drawingMode)
        else:
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
        for i in range(1):
            x0 = random.randrange(100, mode.width-blockW)
            y0 = random.randrange(0, mode.height-blockH)
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
        mode.setUpBlocks(mode.sBlockW, mode.sBlockH, mode.level)
        # long Blocks:
        #mode.setUpBlocks(mode.lBlockW, mode.lBlockH, mode.level)

        # draw blocks
    
    def checkLine(mode):
        # checks to see if chicken is within range of the line
        cx, cy = mode.chickenx, mode.chickeny
        r = mode.chickenr
        for point in mode.makeLine:
            x, y = point
            if abs(x - cx) < r and abs(y - cy) < r:
                mode.onLine = True
                mode.i = mode.makeLine.index(point)
                return True


    def moveOnLine(mode, index): # moves from point to point on line
        if mode.dx > 0: # moving right
            if index + 1 <= len(mode.makeLine):
                mode.chickenx = mode.makeLine[index][0]
                mode.chickeny = mode.makeLine[index][1] - mode.chickenr
                mode.i += 1
            else:
                mode.chickenx += mode.chickenr
                mode.chickeny += mode.dy
                mode.onLine = False
        else: # moving left
            if index - 1 >= 0:
                mode.chickenx = mode.makeLine[index][0]
                mode.chickeny = mode.makeLine[index][1] - mode.chickenr
                mode.i -= 1
            else:
                mode.chickenx -= mode.chickenr
                mode.chickeny += mode.dy
                mode.onLine = False

    def checkBlock(mode):
        '''
        if right edge of chicken is greater than left edge of block
        if left edge of chicken is less than right edge of block
        if bottom of chicken is between the top and bottom of the block
        # or if the bottom of the chicken is equal to the top of the block
        '''
        rightEdge = mode.chickenx + mode.chickenr
        leftEdge = mode.chickenx - mode.chickenr 
        bottomEdge = mode.chickeny + mode.chickenr
        for block in mode.blocks:
            x0, y0, x1, y1 = block
            if rightEdge > x0 and leftEdge < x1:
                if y1 > bottomEdge >= y0:
                    mode.chickeny = y0 - mode.chickenr
                    mode.onBlock = True
                    mode.currentBlockIndex = mode.blocks.index(block)
                    return True

    def moveOnBlock(mode):
        mode.chickenx += mode.dx
        block = mode.blocks[mode.currentBlockIndex]
        x0, y0, x1, y1 = block
        
        if mode.dx > 0 and mode.chickenx + mode.chickenr >= x1:
            mode.onBlock = False
        elif mode.dx < 0 and mode.chickenx - mode.chickenr <= x0:
            mode.onBlock = False


    def timerFired(mode):
        if mode.go:
            if mode.onLine or mode.checkLine():# 2 conditionals so checkLine() isnt always called
                mode.moveOnLine(mode.i)
            elif mode.onBlock or mode.checkBlock():
                mode.moveOnBlock()
            else: # gravity
                mode.chickeny += mode.dy
                mode.i = 0
                if (mode.chickeny + mode.chickenr) >= mode.height:
                        mode.chickeny = mode.height - mode.chickenr
                        mode.chickenx += mode.dx
            if (mode.chickenx - mode.chickenr < 0) or ((mode.chickenx + mode.chickenr) > mode.width):
                    mode.dx = -mode.dx



    def redrawAll(mode, canvas):
        # blocks
        for block in mode.blocks:
            (x0, y0, x1, y1) = block
            shortBlock = PhotoImage(file='short-block.png')
            canvas.create_image(x0, y0, image=shortBlock, anchor = NW)

        #  mode button
        drawing = PhotoImage(file='drawing.png')
        canvas.create_image(mode.width-10, 10, image=drawing, anchor=NE)
        
        # line
        for i in range(1, len(mode.makeLine) - 1):
            if mode.makeLine[i + 1] != None:
                x1, y1 = mode.makeLine[i]
                x2, y2 = mode.makeLine[i + 1]
                canvas.create_line(x1, y1, x2, y2, width=7)
        # chicken
        char = PhotoImage(file=mode.chicken)
        canvas.create_image(mode.chickenx, mode.chickeny, image=char)

        
        
        
 
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