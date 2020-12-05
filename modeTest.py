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
                        


class GameMode(Mode):
    def appStarted(mode):

        mode.muffinx = 0
        mode.muffiny = 0
        mode.chicken = 'chicken.png'
        mode.chickenSize = 50
        mode.chickenr = 10
        mode.dx = 7
        mode.dy = 20
        mode.offScreen = -100

        mode.mouseMovedDelay = 0
        mode.timerDelay = 10

        mode.sBlockW = 100
        mode.sBlockH = 74
        mode.lBlockW = 200
        mode.lBlockH = 74
        mode.level = 1
        mode.blocks = []

        mode.helpOn = True

        mode.stickerOn = False

        mode.load()

        mode.makeBlocks()
        mode.makeMuffin()


    def load(mode):
        # initializes game
        mode.go = False
        mode.penDown = False
        mode.makeLine = []
        mode.newLevel = True
        mode.progress = False
        mode.chickenx = 80
        mode.chickeny = 350
        
        mode.currentBlockIndex = 0
        mode.i = 0
        mode.onLine = False
        mode.onBlock = False
        mode.chickenPath = []





    def keyPressed(mode, event):
        if event.key == 'h':
            mode.penDown = False
            mode.helpOn = not mode.helpOn
        elif event.key == 'r':
            mode.load()
            '''mode.makeLine.clear()
            mode.newLevel = True
            mode.go = False
            mode.chickenx = 70
            mode.chickeny = 70'''
            
    def mousePressed(mode, event):
        if ((mode.width-110) < event.x < (mode.width-10) and
            10 < event.y < 110):
            mode.app.setActiveMode(mode.app.drawingMode)
        else:
            if mode.newLevel:
                mode.penDown = not mode.penDown
                if mode.penDown:
                    x1, y1 = event.x, event.y
                    mode.makeLine.append((x1, y1))
                if not mode.penDown: 
                    mode.go = True
                    if len(mode.makeLine) != 0:
                        mode.newLevel = False

    def mouseMoved(mode, event):
        if mode.penDown:
            x, y = event.x, event.y
            mode.makeLine.append((x, y))

    def setUpBlocks(mode, blockW, blockH, level):

        mode.blocks = [(100, 100, 100 + blockW, 100 + blockH), (200, mode.height-blockH, 200+ blockW, mode.height), (150, 200, 120 + blockW, 200+blockH)]
        '''for i in range(3):
            x0 = random.randint(0, mode.width-blockW - blockW)
            y0 = random.randint(100, mode.height-blockH)
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
            if mode.width-100 < x1 < mode.width and 0 < y0 < 100:
                mode.blocks.remove(newBlock)'''

    def makeBlocks(mode):
        # small Blocks:
        mode.setUpBlocks(mode.sBlockW, mode.sBlockH, mode.level)
        mode.tempBlocks = mode.blocks
        # long Blocks:
        #mode.setUpBlocks(mode.lBlockW, mode.lBlockH, mode.level)

    def setUpMuffin(mode, muffinr):
        x0, y0, x1, y1 = mode.blocks[0]
        mode.muffinx = x1 - muffinr
        mode.muffiny = y0 -muffinr

    def makeMuffin(mode):
        mode.setUpMuffin(mode.chickenr)
    
    def checkMuffin(mode):
        cx, cy = mode.chickenx, mode.chickeny
        mx, my = mode.muffinx, mode.muffiny
        r = mode.chickenr
        if (abs(cx - mx) <= (2*r)) and (abs(cy - my) <= (2*r)):
            return True
    
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
        rightEdge = mode.chickenx 
        leftEdge = mode.chickenx 
        bottomEdge = mode.chickeny + mode.chickenr
        for block in mode.blocks:
            x0, y0, x1, y1 = block
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
            x0, y0, x1, y1 = block
            if (mode.dx > 0 and abs(x0 - rightEdge) < mode.dx ) or (mode.dx < 0 and abs(x1 - leftEdge) < abs(mode.dx)):
                if y0 <= topEdge <= y1 or y0 <= bottomEdge <= y1:
                    mode.i = 0
                    return True


    def timerFired(mode):
        if mode.go:
            if mode.checkMuffin() or mode.onLine or mode.checkLine() or mode.onBlock or mode.checkBlock() or mode.checkWall():
                if mode.checkMuffin():
                    print('muffin')
                    # moving muffin off screen
                    mode.muffinx = mode.offScreen
                    mode.muffiny = mode.offScreen
                    mode.progress = True
                if mode.onLine or mode.checkLine():# 2 conditionals so checkLine() isnt always called
                    print('------LINE------')
                    mode.moveOnLine(mode.i)
                elif mode.onBlock or mode.checkBlock():
                    print('----BLOCK----')
                    mode.moveOnBlock()
                if mode.checkWall():
                    print('HIT A WALL')
                    mode.dx = -mode.dx

            else: # gravity
                print('else')
                mode.chickeny += mode.dy
                mode.i = 0
                if (mode.chickeny + mode.chickenr) >= mode.height:
                    mode.chickeny = mode.height - (.5 * mode.chickenSize)
                    mode.chickenx += mode.dx
                if (mode.chickenx - mode.chickenr < 0):
                    mode.dx = 7
                    mode.i = 0
                elif ((mode.chickenx + mode.chickenr) > mode.width):
                    mode.dx = -7
                    mode.i = 0
                


            

    def redrawAll(mode, canvas):
        background = PhotoImage(file='background.png')
        canvas.create_image(mode.width/2, mode.height/2, image=background)

        for block in mode.blocks:
            (x0, y0, x1, y1) = block
            shortBlock = PhotoImage(file='short-block.png')
            canvas.create_image(x0, y0, image=shortBlock, anchor = NW)

        if mode.stickerOn:
            canvas.create_rectangle(mode.width/2 -20, mode.height/2 -10, mode.width/2 +20, mode.height/2 +10, fill='blue')
            canvas.create_text(mode.width/2, mode.height/2, text='NEXT', fill='white')

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

            


        


class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        app.setActiveMode(app.splashScreenMode)
        app.drawingMode = DrawingMode()


def main():
    app = MyModalApp(width=500, height=500)

if __name__ == '__main__':
    main()