from tkinter import *


class Player:
    score = 0

    def __init__(self, name, frame):
        self.name = name
        self.frame = frame

    def render_player(self):
        title = Label(self.frame, text="Player 1", font=2, bg="aquamarine")
        title.grid(row=0, columnspan=2)
        label = Label(self.frame, text=self.name, font=1.5)
        label.grid(row=1, column=1)