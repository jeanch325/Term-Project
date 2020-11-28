#===============================IMPORTS=================================
import random
import tkinter
from cmu_112_graphics import *
import PIL

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
        in main function, when calling chicken.gravity(), 
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

def keyPressed(app, event):
    if event.key == "Enter":
        app.welcomePageOn = False

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

def drawWelcomePage(app, canvas):
    canvas.create_text(app.width/2, app.height/2, 
                        text='welcome page\nclick enter to begin', 
                        font='Arial 20 bold')

def redrawAll(app, canvas):
    if app.welcomePageOn:
        drawWelcomePage(app, canvas)


#==============================MAIN================================

def main():
    # hard variables 
    height = 400
    width = 600
    blockW = 75
    blockH = 50

    # soft variables
    level = 5
    blocks = []
    runApp(width=700, height=700)

if __name__ == "__main__":
    main()