from cmu_112_graphics import *
import random


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

class GameMode(Mode):
    def appStarted(mode):
        mode.penDown = False

        mode.makeLine = []
        mode.newLevel = True

        mode.chickenx = 5
        mode.chickeny = 5
        mode.chickenSize = 50
        mode.direction = 'right'
        mode.dx = 7
        mode.dy = 15 # gravity ??

        mode.go = False



    def keyPressed(mode, event):
        if event.key == 'h':
            mode.penDown = False
            mode.app.setActiveMode(mode.app.helpMode)
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

    def makeBlocks(mode, canvas, level, blocks):
        for i in range(level):
            x0 = random.randrange(width-blockW)
            y0 = random.randrange(height-blockH)
            x1 = x0 + blockW
            y1 = y0 + blockH
            newBlock = (x0, y0, x1, y1)
            blocks.append(newBlock)
            for oldBlock in blocks:
                xRange = oldBlock[2] - oldBlock[0] 
                yRange = oldBlock[3] - oldBlock[1]
                if ((x0 in range(xRange) or x1 in range(xRange)) and
                    y0 in range(yRange) or y1 in range(yRange)):
                    blocks.remove(newBlock)
            canvas.create_rectangle(x0, y0, x1, y1)


    def moveChicken(mode):
        movingRight = True # for which way chicken is facing & to fall off edge of line or block
        mode.chickenx += mode.dx
        if (mode.chickenx < 0) or ((mode.chickenx + 
                        mode.chickenSize) > mode.width): 
            mode.dx = -mode.dx
            if mode.dx > 0:
                movingRight = True
            else:
                movingRight = False
        # to consider:
        # - if on top of line
        # - edge of line ... chicken should fall down 
        # - if line is vertical
        # - if incline of line is too much
        # - 
        for point in mode.makeLine:
            x, y = point
            if abs(x - mode.chickenx) <= mode.dx: 
                mode.chickeny = y - mode.chickenSize
                
    ''' 
    def move(x, y, isFalling, makeLine, movingRight, movingLeft):
        if isFalling == True:
            if abs(y - (mode.chickeny + mode.chickenSize)) <= mode.dy:
                return isFalling == False # ??
            elif (mode.chickeny + mode.chickenSize) >= mode.height:
                return isFalling = False # ??
        else:
            if makeLine[0][0] < makeLine[-1][0]:
                leftEdge = makeLine[0][0]
                rightEdge = makeLine[-1][0]
            else:
                leftEdge = makeLine[-1][0]
                rightEdge = makeLine[0][0]
            if ((movingRight and (mode.chickenx + mode.chickenSize + mode.dx) >= rightEdge)
                    or (movingLeft and ((mode.chickenx + mode.dx) <= leftEdge))):
                    return isFalling = True
                
                *** how to apply to lines that loopdydoop ????????????????? ***
                
    
    '''


    def gravity(mode):
        if not (mode.chickeny + mode.chickenSize) >= mode.height:
            mode.chickeny += mode.dy 

    def timerFired(mode):
        if mode.go:
            mode.moveChicken()



    def redrawAll(mode, canvas):
        for i in range(1, len(mode.makeLine) - 1):
            if mode.makeLine[i + 1] != None:
                x1, y1 = mode.makeLine[i]
                x2, y2 = mode.makeLine[i + 1]
                canvas.create_line(x1, y1, x2, y2, width=7)
        chicken = PhotoImage(file='chicken.png')
        canvas.create_image(mode.chickenx, mode.chickeny, image=chicken, anchor=NW)

class HelpMode(Mode):
    def redrawAll(mode, canvas):
        canvas.create_rectangle(mode.width/2 - 120, mode.height/2 - 120, 
                                mode.width/2 + 160, mode.height/2 + 160, fill='blue')
        canvas.create_rectangle(mode.width/2 - 140, mode.height/2 - 140, 
                                mode.width/2 + 140, mode.height/2 + 140, fill='white')

        canvas.create_text(mode.width/2, mode.height/2 - 120, text='HELP PAGE', font='Arial 20 bold') 
        canvas.create_text(mode.width/2, mode.height/2 - 90, text='* press r to restart') 
        canvas.create_text(mode.width/2, mode.height/2 - 60, text='* press h to access/leave help page')
        canvas.create_text(mode.width/2, mode.height/2 - 30, text='* click once to put pen down') 
        canvas.create_text(mode.width/2, mode.height/2 - 10 , text='and move mouse to draw.') 
        canvas.create_text(mode.width/2, mode.height/2 + 20, text='* click again to lift pen up') 
        canvas.create_text(mode.width/2, mode.height/2 + 40, text='and stop drawing.') 
        canvas.create_text(mode.width/2, mode.height/2 + 70, text='* you have 1 pen per level!') 

    def keyPressed(mode, event):
        if event.key == 'h':
            mode.app.setActiveMode(mode.app.gameMode)

class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        app.helpMode = HelpMode()
        app.setActiveMode(app.splashScreenMode)

app = MyModalApp(width=500, height=500)