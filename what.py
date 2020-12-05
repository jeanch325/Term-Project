from tkinter import *
from PIL import Image, ImageDraw

width = 400
height = 300
center = height//2
white = (255, 255, 255)
green = (0,128,0)

root = Tk()

# Tkinter create a canvas to draw on
cv = Canvas(root, width=width, height=height, bg='white')
cv.pack()

# PIL create an empty image and draw object to draw on
# memory only, not visible
image1 = Image.new("RGB", (width, height), white)
draw = ImageDraw.Draw(image1)

# do the Tkinter canvas drawings (visible)
for row in range(mode.rows):
    for col in range(mode.cols):
        (x0, y0, x1, y1) = mode.getCellBounds(row, col)
        for point in mode.draw:
            x, y, color = point
            if mode.checkPoint(x, y, x0, y0, x1, y1):
                canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=0)
                rgbColor = PIL.ImageColor.getrgb(color)
                ImageDraw.polygon([(x0, y0), (x1, y1)], fill=rgbColor, outline=None)

# do the PIL image/draw (in memory) drawings
for row in range(mode.rows):
    for col in range(mode.cols):
        (x0, y0, x1, y1) = mode.getCellBounds(row, col)
        for point in mode.draw:
            x, y, color = point
            rgbColor = PIL.ImageColor.getrgb(color)
            if mode.checkPoint(x, y, x0, y0, x1, y1):
                ImageDraw.polygon([(x0, y0), (x1, y1)], fill=rgbColor, outline=None)
# PIL image can be saved as .png .jpg .gif or .bmp file (among others)
filename = "my_drawing.jpg"
image1.save(filename)

