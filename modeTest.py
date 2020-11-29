from cmu_112_graphics import *
import random

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


    def keyPressed(mode, event):
        if event.key == 'h':
            mode.penDown = False
            mode.app.setActiveMode(mode.app.helpMode)
        elif event.key == 'r':
            mode.makeLine.clear()
            
    def mousePressed(mode, event): 
        if mode.newLevel:
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


    def drawLine(mode, canvas): 
        for i in range(1, len(mode.makeLine) - 1):
            if mode.makeLine[i + 1] != None:
                x1, y1 = mode.makeLine[i]
                x2, y2 = mode.makeLine[i + 1]
                canvas.create_line(x1, y1, x2, y2)


    def drawChicken(mode, canvas):
        # code to upload images is from https://stackoverflow.com/questions/43009527/how-to-insert-an-image-in-a-canvas-item
        chicken = PhotoImage(file='chicken.png')
        canvas.create_image(mode.chickenx, mode.chickeny, image=chicken, anchor=NW)

    def moveChicken(mode):
        mode.x += mode.dx
        if (mode.x < 0) or (mode.x > mode.width): mode.dx = -mode.dx
        mode.y += mode.dy
        if (mode.y < 0) or (mode.y > mode.height): mode.dy = -mode.dy

    def timerFired(mode):
        mode.moveDot()


    def redrawAll(mode, canvas):
        drawLine(mode, canvas)
        drawChicken(mode, canvas)

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