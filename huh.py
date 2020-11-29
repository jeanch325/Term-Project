#===============================IMPORTS=================================
import random
from tkinter import *
from cmu_112_graphics import *
from PIL import Image
#===============================CLASSES=================================

# SUPER CLASS FOR CHARACTER
class Character(object):
    def __init__(self, name, x, y, charWidth=10, charHeight=20):
        self.name = name
        self.charWidth = charWidth
        self.charHeight = charHeight
        self.x = x
        self.y = y
        
    def __repr__(self):
        return f'{self.name}'
    def __eq__(self, other):
        return isinstance(other, Character) and (self.name == other.name)
    def __hash__(self):
        return hash(self)
    
    def gravity(self): # gravity function
        '''
        in main function, when calling Character.gravity(), 
        check if its x position is touching a block.
        if it is, stop gravity function until the chicken runs off the block 
        '''
        self.y += 10
        if self.y > height:
            self.y = height - self.charHeight
        
    def move(self): # moving left to right
        '''
        in main function, if (self.x +- self.charWidth ) or (self.y +- charHeight)
        == ((for foodx, foody in Food.foods) +- foodSize): call chicken character .eatFood()
        '''
        if self.x > width:
            self.x -= 5
        elif self.x < 0:
            self.x += 5
    
# SUB CLASS FOR CHICKEN
class Chicken(Character):
    def __init__(self, name, x, y, hp, level, charWidth=10, charHeight=20):
        self.hp = 0
        self.level = 1
        super().__init__(self, name, x, y, charWidth=10, charHeight=20)
        
    # eat food
    def eatFood(self):
        self.hp += 10
        
    # level up
    def levelUp(self):
        self.level += 1
        
    # shoot at monster
    def shoot(self):
        self.hp -= 10
        
# SUB CLASS FOR ENEMY
class Enemy(Character):
    enemies = []
    def __init__(self, name, x, y, charWidth=10, charHeight=20):
        super().__init__(self, name, x, y, charWidth=10, charHeight=20)
        Enemy.enemies.append(self.name) # do i have no name all of them :|     
        
    def die(self):
        Enemy.enemies.remove(self.name)
        
# CLASS FOR FOOD
class Star(object):
    stars = []
    def __init__(self, x, y, size=5):
        self.x = x
        self.y = y
        Star.stars.append((self.x, self.y))
        self.size = size
        
    '''
    call in main when eaten ;;;; mentioned above in Chicken.move() already
    '''
    def eaten(self):
        Star.stars.remove((self.x, self.y))

#==============================FUNCTIONS================================

def appStarted(app):
    app.welcomePageOn = True
    app.penDown = False
    app.makeLine = []
    app.helpPageOn = True
    app.newLevel = True

    app.chickenStartx = 5
    app.chickenStarty = 5

def keyPressed(app, event):
    if event.key == "Enter":
        app.welcomePageOn = False
    elif event.key == 'h':
        app.penDown = False
        app.helpPageOn = not app.helpPageOn
    elif event.key == 'r':
        app.makeLine.clear()
        app.newLevel = True
        
def mousePressed(app, event): 
    if app.newLevel:
        app.penDown = not app.penDown
        if app.penDown:
            print('hi')
        if app.penDown:
            x1, y1 = event.x, event.y
            app.makeLine.append((x1, y1))
        if not app.penDown and len(app.makeLine) != 0:
            app.newLevel = False

def mouseMoved(app, event):
    if app.penDown:
        x, y = event.x, event.y
        app.makeLine.append((x, y))
        print(app.makeLine)

def makeBlocks(app, canvas, level, blocks):
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


def drawLine(app, canvas): 
    for i in range(1, len(app.makeLine) - 1):
        if app.makeLine[i + 1] != None:
            x1, y1 = app.makeLine[i]
            x2, y2 = app.makeLine[i + 1]
            canvas.create_line(x1, y1, x2, y2)

def drawHelpPage(app, canvas):
    canvas.create_rectangle(app.width/2 - 120, app.height/2 - 120, 
                            app.width/2 + 160, app.height/2 + 160, fill='blue')
    canvas.create_rectangle(app.width/2 - 140, app.height/2 - 140, 
                            app.width/2 + 140, app.height/2 + 140, fill='white')

    canvas.create_text(app.width/2, app.height/2 - 120, text='HELP PAGE', font='Arial 20 bold') 
    canvas.create_text(app.width/2, app.height/2 - 90, text='* press r to restart') 
    canvas.create_text(app.width/2, app.height/2 - 60, text='* press h to access/leave help page')
    canvas.create_text(app.width/2, app.height/2 - 30, text='* click once to put pen down') 
    canvas.create_text(app.width/2, app.height/2 - 10 , text='and move mouse to draw.') 
    canvas.create_text(app.width/2, app.height/2 + 20, text='* click again to lift pen up') 
    canvas.create_text(app.width/2, app.height/2 + 40, text='and stop drawing.') 
    canvas.create_text(app.width/2, app.height/2 + 70, text='* you have 1 pen per level!') 

def drawChicken(app, canvas):
    # code to upload images is from https://stackoverflow.com/questions/43009527/how-to-insert-an-image-in-a-canvas-item
    chicken = PhotoImage(file='chicken.png')
    canvas.create_image(app.chickenStartx, app.chickenStarty, image=chicken, anchor=NW)


def drawWelcomePage(app, canvas):
    canvas.create_text(app.width/2, app.height/2, 
                        text='welcome page\nclick enter to begin', 
                        font='Arial 20 bold')

def redrawAll(app, canvas):
    if app.welcomePageOn:
        drawWelcomePage(app, canvas)
    elif app.helpPageOn:
        drawHelpPage(app, canvas)
    else:
        drawLine(app, canvas)
        drawChicken(app, canvas)

            


#==============================MAIN================================

def main():
    # hard variables 
    height = 600
    width = 800
    blockW = 75
    blockH = 50


    # soft variables
    level = 5
    blocks = []
    runApp(width=width, height=height)

    # functions
    


if __name__ == "__main__":
    main()