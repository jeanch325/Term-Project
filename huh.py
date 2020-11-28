from cmu_112_graphics import *

def appStarted(app):
    app.welcomePageOn = True

def keyPressed(app, event):
    if event.key == "Enter":
        app.welcomePageOn = False

def drawWelcomePage(app, canvas):
    canvas.create_text(app.width/2, app.height/2, 
                        text='welcome page\nclick enter to begin', 
                        font='Arial 20 bold')

def redrawAll(app, canvas):
    if app.welcomePageOn:
        drawWelcomePage(app, canvas)

runApp(width=700, height=700)