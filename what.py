import tkinter as tk

class PicTest:
    def __init__(self, name, image):
        self.name = name
        self.image = tk.PhotoImage(file=image)

root = tk.Tk()
foo = PicTest('foo', 'chicken.png')

def testwindow():
    foo_testlabel = tk.Label(root, image=foo.image)
    foo_testlabel.pack()

testwindow()
root.mainloop()

# how to assign image to class ???????????????????????