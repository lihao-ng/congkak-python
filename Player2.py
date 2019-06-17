from tkinter import *


class Player:
    score = 0

    def __init__(self, name, frame):
        self.name = name
        self.currentScore = 0
        self.frame = frame

    def assignScore(self, score):
        self.currentScore += score

    def assignRemaining(self, barray):
        for i in barray:
            self.currentScore += i.beads
            i.beads = 0

    def render_player(self):
        label = Label(self.frame, text=self.name, font=1.5)
        label.grid(row=0, column=0)
        label = Label(self.frame, text=self.currentScore, font=3)
        label.grid(row=1, column=0)