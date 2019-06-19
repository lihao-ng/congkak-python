from tkinter import *
from PIL import Image, ImageTk

class Player:
    score = 0

    def __init__(self, name, frame):
        self.name = name
        self.currentScore = 0
        self.frame = frame

        if(self.name == "Player_1"):
            image = Image.open("images/edge-left.png").resize((200, 341), Image.ANTIALIAS)
        else:
            image = Image.open("images/edge-right.png").resize((200, 341), Image.ANTIALIAS)
        loadImage = ImageTk.PhotoImage(image)

        self.renderScore = Label(self.frame, image=loadImage, text=self.currentScore, compound=CENTER, font=3, bd=-2, fg="white", bg="#ffffe0", pady=0, padx=0)
        self.renderScore.config(font=("Courier", 44))
        self.renderScore.photo = loadImage
        self.renderScore.pack(side=TOP, expand=YES, fill=BOTH)

    def assignScore(self, score):
        self.currentScore += score

    def assignRemaining(self, barray):
        for i in barray:
            self.currentScore += i.beads
            i.beads = 0

    def render_player(self):
        self.renderScore.configure(text=self.currentScore)
        # image = Image.open("images/hole.png").resize((150, 150), Image.ANTIALIAS)
        # loadImage = ImageTk.PhotoImage(image)
        #
        # label = Label(self.frame, text=self.name, font=1.5, height=3, bg="#ffffe0")
        # label.grid(row=0, column=0)
        # label = Label(self.frame, image=loadImage, text=self.currentScore, compound=CENTER, font=3, fg="white", bg="#ffffe0")
        # label.config(font=("Courier", 44))
        # label.photo = loadImage
        # label.grid(row=2, column=0, pady=20)