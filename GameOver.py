from tkinter import *

class GameOver(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        gameOverFrame = Frame(self)
        label = Label(self, text="Game Over", compound=CENTER, font=2.5, bg="#866538", fg="white")
        label.pack()
        gameOverFrame.pack()