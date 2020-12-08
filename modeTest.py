from cmu_112_graphics import *
import random
import time
from PIL import Image, ImageDraw, ImageColor


# mode class structure is from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#subclassingModalApp

class SplashScreenMode(Mode):
    def redrawAll(mode, canvas):
        splash = PhotoImage(file='splash.png')
        canvas.create_image(mode.width/2, mode.height/2, image=splash)
        canvas.create_text(mode.width/2, mode.height/2 - 80, text='WELCOME TO', font='Arial 50 bold')
        canvas.create_text(mode.width/2, mode.height/2 - 30, text='CHICKEN HIKE', font='Arial 60 bold')
        canvas.create_text(mode.width/2, mode.height/2 + 20, text='press enter to begin', font='Arial 20 bold')

    def keyPressed(mode, event):
        if event.key == 'Enter':
            mode.app.setActiveMode(mode.app.instructionsMode)

class InstructionsMode(Mode):

    def appStarted(mode):
        mode.screen1 = True
        mode.screen2 = False
        mode.screen3 = False
        mode.screen4 = False

        mode.arrowx0 = 250
        mode.arrowx1 = 260

        mode.linex0 = 130
        mode.linex1 = 140

    def keyPressed(mode, event):
        if event.key == 'Right':
            if mode.screen1:
                mode.screen1 = False
                mode.screen2 = True
            elif mode.screen2:
                mode.screen2 = False
                mode.screen3 = True
            elif mode.screen3:
                mode.screen3 = False
                mode.screen4 = True
            elif mode.screen4:
                mode.app.setActiveMode(mode.app.gameMode)
        elif event.key == 'Left':
            if mode.screen2:
                mode.screen2 = False
                mode.screen1 = True
            elif mode.screen3:
                mode.screen3 = False
                mode.screen2 = True
            elif mode.screen4:
                mode.screen4 = False
                mode.screen3 = True

    def timerFired(mode):
        mode.arrowx1 += 10
        if mode.arrowx1 == 320:
            mode.arrowx1 = 260
        mode.linex1 += 10
        if mode.linex1 == 370:
            mode.linex1 = 140


    def redrawAll(mode, canvas):
        screen1 = PhotoImage(file='screen1.png')
        screen2 = PhotoImage(file='screen2.png')
        screen3 = PhotoImage(file='screen3.png')
        screen3help = PhotoImage(file='screen3-help.png')
        screen4 = PhotoImage(file='screen4.png')

        if mode.screen1 == True:
            canvas.create_image(mode.width/2, mode.height/2, image=screen1)
            canvas.create_text(mode.width/2, 100, 
            text='         This is Bradley \nthe moonwalking chicken.', 
            font='Arial 30 bold')
            canvas.create_text(mode.width/2, mode.height-100, 
            text='All Bradley wants to do \n      is to eat muffins.', 
            font='Arial 30 bold')
            canvas.create_text(mode.width/2, mode.height-50, 
            text='(Use the arrow keys to mode to navigate between slides)', 
            font='Arial 15 bold')

        if mode.screen2 == True:
            canvas.create_image(mode.width/2, mode.height/2, image=screen2)
            canvas.create_text(mode.width/2, 70, 
            text='  Help him get to the muffin by \nusing your mouse to draw a line', 
            font='Arial 20 bold')
            canvas.create_text(mode.width/2, 105, 
            text=' for him to walk on.', 
            font='Arial 20 bold')
            canvas.create_text(mode.width/2, 170, 
            text='    You can draw lines by \nclicking and releasing once,', 
            font='Arial 30 bold')
            canvas.create_text(mode.width/2, 235, 
            text='       dragging, and then \nclicking and releasing again', 
            font='Arial 30 bold')
            canvas.create_text(mode.width/2, 285, 
            text='to finish drawing.', 
            font='Arial 30 bold')
            canvas.create_text(mode.width/2, 320, 
            text='You only have 1 line per level!', 
            font='Arial 30 bold')
            canvas.create_line(mode.linex0, 400, mode.linex1, 400, width=15)
            canvas.create_image(mode.linex1, 410, image=mouse)

        if mode.screen3 == True:
            canvas.create_image(mode.width/2, mode.height/2, image=screen3)
            canvas.create_image(127, mode.height - 125, image=screen3help)
            canvas.create_text(mode.width/4, 290, 
            text='If you\'re tired of Bradley,', 
            font='Arial 18 bold')
            canvas.create_text(mode.width/4, 330, 
            text='you can create your own\ncharacter by switching to\ndrawing mode by clicking', 
            font='Arial 18 bold')
            canvas.create_text(mode.width/4, 395, 
            text='the Drawing Mode button\n at the top right corner\n         of the screen!', 
            font='Arial 18 bold')
            canvas.create_text(mode.width/4, 440, 
            text='Bradley will miss you :\'(', 
            font='Arial 18 bold')
            canvas.create_line(mode.arrowx0, 50, mode.arrowx1, 50, fill='red', width=10)
            canvas.create_text(mode.arrowx1 - 3, 50, text ='>', 
            font='Arial 30 bold', fill='red')

        if mode.screen4 == True:
            canvas.create_image(mode.width/2, mode.height/2, image=screen4)
            canvas.create_text(mode.width/2, 100, 
            text='Press the Right Arrow key \n               to play!', 
            font='Arial 30 bold')

    
            

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
        # list of colors from https://stackoverflow.com/questions/732192/get-tk-winfo-rgb-without-having-a-window-instantiated
        mode.colors = [['#CD0000', '#FF0000', '#FF6347'], 
                        ['#FF8C00', '#FFA500', '#FFD700'], 
                        ['#FFFF00', '#CD9B1D', '#6B8E23'], 
                        ['#006400', '#32CD32', '#00FF00'], 
                        ['#76EEC6', '#63B8FF', '#1E90FF'], 
                        ['#0000FF', '#0000CD', '#000080'], 
                        ['#6959CD', '#7D26CD', '#A020F0'], 
                        ['#9A32CD', '#EE00EE', '#EE3A8C'], 
                        ['#FF34B3', '#FF82AB', '#FF69B4'], 
                        ['#000000', '#3B3B3B', '#9E9E9E'], 
                        ['#D9D9D9', '#FFFFFF', '#8B1A1A'], 
                        ['#8B4726', '#FF8247', '#FFDEAD']]

        mode.newDrawing = True
        mode.spriteImage = None
        mode.startSpriteDrawing = None


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

        # creating new image for sprite
        # from https://stackoverflow.com/questions/9886274/how-can-i-convert-canvas-content-to-an-image
        if mode.newDrawing == True:
            mode.spriteImage = Image.new("RGB", (mode.width, mode.height), (0, 0, 0, 0))
            # putalpha is transparency. code from https://note.nkmk.me/en/python-pillow-putalpha/ 
            mode.spriteImage.putalpha(0)
            mode.startSpriteDrawing = ImageDraw.Draw(mode.spriteImage)
            mode.newDrawing = False
 
        # drawing lines
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
        if event.key == 'Enter':
            mode.app.setActiveMode(mode.app.gameMode)
        elif event.key == 's':
            mode.exportSprite()
        elif event.key == 'e':
            mode.penType = 'eraser'
        elif event.key == 'p':
            mode.penType = 'pen'
    
    def exportSprite(mode):
        # image crop code: https://stackoverflow.com/questions/9983263/how-to-crop-an-image-using-pil 

        sprite = mode.spriteImage.crop((100, 100, mode.width, mode.height)) 

        # image thumbnail code: https://www.geeksforgeeks.org/python-pil-image-thumbnail-method/        
        sprite.thumbnail((50, 50)) 
        filename = "newcharacter.png"
        sprite.save(filename)
        mode.app.gameMode.chicken = 'newcharacter.png'

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
        canvas.create_text(290, 50, text='fill drawing to edges of canvas!', font='Arial 15', anchor=NW)

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
                        rgbColor = ImageColor.getrgb(color)
                        mode.startSpriteDrawing.rectangle([(x0, y0), (x1, y1)], fill=rgbColor)
                        


# code w Kosbie 12/5/2020
def distance(x1, y1, x2, y2):
    return (((x2-x1)**2 + (y2-y1)**2)** 0.5)

def lineSegmentIntersectsCircle(x0, y0, x1, y1, cx, cy, r):
    if x1 == x0:
        # they're the same point, so if point intersects circle
        return distance(x0, y0, cx, cy) <= r
    m = (y1 - y0) / (x1 - x0)
    b = y0 - m*x0
    # now we know the line is: y = mx + b
    A = (1 + m**2)
    B = -2*cx + 2*b*m - 2*cy*m
    C = cx**2  + b**2  - 2*b*cy + cy**2 - r**2

    if (B**2 - 4*A*C) < 0:
        # (the entire line did not hit the circle)
        #print('2')
        return False

    x2 = (-B + (B**2 - 4*A*C)**0.5) / (2*A)
    x3 = (-B - (B**2 - 4*A*C)**0.5) / (2*A)
    y2 = m*x2+b
    y3 = m*x3+b
    return (x0 <= x2 <= x1) or (x0 <= x3 <= x1) or (x0 >= x2 >= x1) or (x0 >= x3 >= x1)

def findSlope(x1, y1, x2, y2):
    rise = abs(y2 - y1)
    run = abs(x2 - x1)
    try:
        return rise/run

    except ZeroDivisionError:
        return 100

class GameMode(Mode):
    def appStarted(mode):

        mode.bluex = mode.width/2
        mode.purplex = mode.bluex - mode.width
        mode.pinkx = mode.purplex - mode.width

        mode.switchLevels = False

        mode.verticalLineApproached = False

        mode.muffinx = 0
        mode.muffiny = 0
        mode.chicken = 'chicken.png'
        mode.chickenSize = 50
        mode.chickenr = 10
        mode.dy = 20
        mode.offScreen = -100

        mode.mouseMovedDelay = 0
        mode.timerDelay = 10

        mode.sBlockW = 100
        mode.sBlockH = 74
        mode.level = 2
        mode.youDiedOn = False

        mode.helpOn = True

        mode.load()

    def load(mode):
        # initializes game
        mode.progress = False
        mode.blocks = []
        
        mode.restart()
        mode.placeBlocks()
        mode.makeMuffin()

    def restart(mode):
        mode.newLevel = True
        mode.makeLine = []
        mode.go = False
        mode.penDown = False
        mode.chickenx = 100
        mode.chickeny = 100
        mode.currentBlockIndex = 0
        mode.i = 0
        mode.onLine = False
        mode.onBlock = False
        mode.chickenPath = []
        mode.dx = 7

 




    def keyPressed(mode, event):
        if event.key == 'h':
            mode.penDown = False
            mode.helpOn = not mode.helpOn
        elif event.key == 'r':
            mode.restart()
        elif event.key == 'Enter' and mode.youDiedOn == True:
            mode.youDiedOn = False
            mode.restart()
        elif event.key == 'Left':
            mode.app.setActiveMode(mode.app.instructionsMode)
            
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
                if not mode.penDown: 
                    if len(mode.makeLine) != 0:
                        mode.newLevel = False

    def mouseMoved(mode, event):
        if mode.penDown:
            x, y = event.x, event.y
            mode.makeLine.append((x, y))

    # new blocks code
    def getCellBoundsForBlocks(mode, row, col):
        cellWidth = mode.width / mode.level
        cellHeight = (mode.height-100) /mode.level
        x0 = col * cellWidth
        x1 = (col+1) * cellWidth
        y0 = row * cellHeight + 100
        y1 = (row+1) * cellHeight + 100
        return (x0, y0, x1, y1)

    def chooseBlocksFromList(mode):
        midsList = []
        for row in range(mode.level):
            for col in range(mode.level):
                (x0, y0, x1, y1) = mode.getCellBoundsForBlocks(row, col)
                midsList.append((x0, y0, x1, y1))
        return midsList

    def placeBlocks(mode):
        midsList = mode.chooseBlocksFromList()
        for i in range(mode.level):
            index = random.randrange(0, len(midsList))
            if midsList[index] not in mode.blocks:
                mode.blocks.append(midsList[index])


    def setUpMuffin(mode, muffinr):
        setUp = False
        for block in mode.blocks:
            boundx0, boundy0, boundx1, boundy1 = block
            x0 = (boundx0 + boundx1 - mode.sBlockW) /2 
            x1 = (boundx0 + boundx1 + mode.sBlockW) /2 
            y0 = (boundy0 + boundy1) / 2 - (mode.sBlockH/2)
            y1 = (boundy0 + boundy1) / 2 + (mode.sBlockH/2)
            if x0 > mode.width/2:
                midx = (x0 + x1) /2
                midy = (y0 + y1) / 2
                mode.muffinx = midx
                mode.muffiny = midy - 50
                setUp = True
                break
        if setUp == False:
            x0, y0, x1, y1 = mode.blocks[random.randrange(0, len(mode.blocks))]
            midx = (x0 + x1) /2
            midy = (y0 + y1) / 2
            mode.muffinx = midx
            mode.muffiny = midy - (50)

    def makeMuffin(mode):
        mode.setUpMuffin(mode.chickenr)
    
    def checkMuffin(mode):
        cx, cy = mode.chickenx, mode.chickeny
        mx, my = mode.muffinx, mode.muffiny
        if (abs(cx - mx) <= (mode.chickenSize)) and (abs(cy - my) <= (mode.chickenSize)):
            return True
    
    def lineIsVertical(mode, index):
        if index != (len(mode.makeLine) - 1):
            x1, y1 = mode.makeLine[index]
            x2, y2 = mode.makeLine[index+1]
            slope = findSlope(x1, y1, x2, y2)
            if slope > 7:
                mode.verticalLineApproached = True
                return True
            else:
                return False


    def checkLine(mode):
        if mode.makeLine == []:
            return False
        # checks to see if chicken is within range of the line
        cx, cy = mode.chickenx, mode.chickeny
        r = 25
        prevx, prevy = mode.makeLine[0]
        for point in mode.makeLine:
            x, y = point
            if lineSegmentIntersectsCircle(prevx, prevy, x, y, cx, cy, r):
                mode.i = mode.makeLine.index(point)
                if mode.lineIsVertical(mode.i) == False:
                    mode.onLine = True
                    return True  
        return False



    def moveOnLine(mode, index): # moves from point to point on line
        if mode.dx > 0: # moving right
            if index + 1 <= len(mode.makeLine):
                mode.chickenx = mode.makeLine[index][0]
                mode.chickeny = mode.makeLine[index][1] - mode.chickenr
                mode.i += 1
            else:
                mode.onLine = False
        else: # moving left
            if index - 1 >= 0:
                mode.chickenx = mode.makeLine[index][0]
                mode.chickeny = mode.makeLine[index][1] - mode.chickenr
                mode.i -= 1
            else:
                mode.onLine = False



            

    def checkBlock(mode):
        '''
        if right edge of chicken is greater than left edge of block
        if left edge of chicken is less than right edge of block
        if bottom of chicken is between the top and bottom of the block
        # or if the bottom of the chicken is equal to the top of the block
        '''
        rightEdge = mode.chickenx 
        leftEdge = mode.chickenx 
        bottomEdge = mode.chickeny + mode.chickenr
        for block in mode.blocks:
            boundx0, boundy0, boundx1, boundy1 = block
            x0 = (boundx0 + boundx1 - mode.sBlockW) /2 
            x1 = (boundx0 + boundx1 + mode.sBlockW) /2 
            y0 = (boundy0 + boundy1) / 2 - (mode.sBlockH/2)
            y1 = (boundy0 + boundy1) / 2 + (mode.sBlockH/2)
            if not (rightEdge+20 < x0 or leftEdge-20 > x1):
                if  y0 <= bottomEdge < y1 :
                    mode.chickeny = y0 - mode.chickenr
                    mode.currentBlockIndex = mode.blocks.index(block)
                    return True

    def moveOnBlock(mode):
        mode.chickenx += mode.dx
        block = mode.blocks[mode.currentBlockIndex]
        x0, y0, x1, y1 = block
        
        if mode.dx > 0 and mode.chickenx - mode.chickenr >= x1:
            mode.onBlock = False
        elif mode.dx < 0 and mode.chickenx + mode.chickenr <= x0:
            mode.onBlock = False
   
    def checkWall(mode):
        '''
        if distance from edges of chicken to edges of block < chickens radius
        if left edge of chicken is less than right edge of block
        if bottom of chicken is between the top and bottom of the block
        # or if the bottom of the chicken is equal to the top of the block
        '''
        rightEdge = mode.chickenx + 25
        leftEdge = mode.chickenx - 25
        topEdge = mode.chickeny - 25
        bottomEdge = mode.chickeny + 25
        for block in mode.blocks:
            boundx0, boundy0, boundx1, boundy1 = block
            x0 = (boundx0 + boundx1 - mode.sBlockW) /2 
            x1 = (boundx0 + boundx1 + mode.sBlockW) /2 
            y0 = (boundy0 + boundy1) / 2 - (mode.sBlockH/2)
            y1 = (boundy0 + boundy1) / 2 + (mode.sBlockH/2)
            if (mode.dx > 0 and abs(x0 - rightEdge) < 3 ) or (mode.dx < 0 and abs(x1 - leftEdge) < abs(3)):
                if y0 <= topEdge <= y1 or y0 <= bottomEdge <= y1:
                    mode.i = 0
                    return True


    def timerFired(mode):
        if mode.go:
            if (mode.chickenx - (.5 * mode.chickenSize) < 0):
                mode.dx = 7
                mode.i = 0
            elif ((mode.chickenx + (.5 * mode.chickenSize)) > mode.width):
                mode.dx = -7
                mode.i = 0
            if mode.checkMuffin() or mode.onLine or mode.checkLine() or mode.onBlock or mode.checkBlock() or mode.checkWall():
                if mode.checkMuffin():
                    mode.muffinx = -100
                    mode.switchLevels = True
                    mode.level += 1
                    mode.load()
                if mode.onLine or mode.checkLine():# 2 conditionals so checkLine() isnt always called
                    mode.moveOnLine(mode.i)
                    mode.chickenx += mode.dx 
                    if mode.dx > 0:
                        mode.chickenx += mode.chickenr
                    elif mode.dx < 0:
                        mode.chickenx - mode.chickenr
                elif mode.onBlock or mode.checkBlock():
                    mode.moveOnBlock()
                if mode.checkWall():
                    mode.dx = -mode.dx

            else: # 
                if mode.verticalLineApproached == True:
                    mode.dx = -mode.dx
                    mode.verticalLineApproached = False
                mode.i = 0
                if (mode.chickeny + mode.chickenr) >= mode.height:
                    modechickeny = mode.height - 2 * mode.chickenSize
                    mode.youDiedOn = True
                else:
                    mode.chickeny += mode.dy
                
        if mode.switchLevels:
            mode.sideScroll()
                

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
        mode.bluex += 50
        mode.purplex += 50
        mode.pinkx += 50
        mode.switchBackgrounds()
            

    def redrawAll(mode, canvas):
        # background
        blue = PhotoImage(file='blue.png')
        canvas.create_image(mode.bluex, mode.height/2, image=blue)

        purple = PhotoImage(file='purple.png')
        canvas.create_image(mode.purplex, mode.height/2, image=purple)

        pink = PhotoImage(file='pink.png')
        canvas.create_image(mode.pinkx, mode.height/2, image=pink)

        # blocks
        shortBlock = PhotoImage(file='short-block.png')
        for block in mode.blocks:
            (x0, y0, x1, y1) = block
            midx = (x0 + x1) /2
            midy = (y0 + y1) / 2
            canvas.create_image(midx, midy, image=shortBlock)

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

        # muffin
        muffin = PhotoImage(file='muffin.png')
        canvas.create_image(mode.muffinx, mode.muffiny, image=muffin)

        # help page
        help = PhotoImage(file='help.png')
        if mode.helpOn:
            loc = 25
            mid = mode.height/2
            canvas.create_image(mode.width/2, mode.height/2, image=help)
            canvas.create_text(mode.width/2, mid-(loc * 4), text='HELP PAGE', font='Arial 20 bold') 
            canvas.create_text(mode.width/2, mid-(loc * 3), text='* press r to restart') 
            canvas.create_text(mode.width/2, mid-(loc * 2), text='* press h to access/leave help page')
            canvas.create_text(mode.width/2, mid-(loc), text='* click once to put pen down') 
            canvas.create_text(mode.width/2, mid-5, text='and move mouse to draw.') 
            canvas.create_text(mode.width/2, mid+(loc)-5, text='* click again to lift pen up') 
            canvas.create_text(mode.width/2, mid+(loc * 2)-10, text='and stop drawing.') 
            canvas.create_text(mode.width/2, mid+(loc * 3)-10, text='* you have 1 pen per level!') 

        # you died
        if mode.youDiedOn == True:
            youlost = PhotoImage(file='youlost.png')
            canvas.create_image(mode.width/2, mode.height/2, image=youlost)
            canvas.create_text(mode.width/2, mode.width/2 - 50, text='YOU LOST :(', font='Arial 35 bold') 
            canvas.create_text(mode.width/2, mode.width/2 - 10 , text='press Enter to restart level', 
                                                        font='Arial 15 bold') 
            
            


class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        app.instructionsMode = InstructionsMode()
        app.drawingMode = DrawingMode()
        app.setActiveMode(app.splashScreenMode)


def main():
    app = MyModalApp(width=500, height=500)

if __name__ == '__main__':
    main()