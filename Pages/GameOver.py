from tkinter import *
from PIL import Image, ImageTk

class GameOver(Frame):

    def __init__(self, parent, controller, **kwargs):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#ffffe0")

        self.player1Score = kwargs.get("player1Score")
        self.player2Score = kwargs.get("player2Score")
        self.player2Name = kwargs.get("player2Name")
        self.p2WinnerImage = None
        if self.player2Name == "CPU":
            self.p2WinnerImage = Image.open("images/CPU-winner.png").resize((200, 120), Image.ANTIALIAS)
        else:
            self.p2WinnerImage = Image.open("images/Player2-winner.png").resize((200, 120), Image.ANTIALIAS)

        self.background = "#b2854b"

        gameOverImage = Image.open("images/Game-Over.png").resize((700, 180), Image.ANTIALIAS)
        loadGameOverImage = self.loadImage(gameOverImage)

        p1WinnerImage = Image.open("images/Player1-winner.png").resize((200, 120), Image.ANTIALIAS)
        loadp1WinnerImage = self.loadImage(p1WinnerImage)

        loadp2WinnerImage = self.loadImage(self.p2WinnerImage)

        image = Image.open("images/hole.png").resize((200, 200), Image.ANTIALIAS)
        loadImage = ImageTk.PhotoImage(image)

        plankImage = Image.open("images/plank.png").resize((275, 50), Image.ANTIALIAS)
        loadPlankImage = ImageTk.PhotoImage(plankImage)

        gameOverFrame = Frame(self, bg=self.background)
        resultFrame = Frame(gameOverFrame, bg="#b2854b")

        label = Label(resultFrame, image=loadGameOverImage, bg=self.background, bd=-2)
        label.photo = loadGameOverImage
        label.grid(row=0, columnspan=12, pady=0, padx=0)

        label = Label(resultFrame, image=loadp1WinnerImage, bg=self.background)
        label.photo = loadp1WinnerImage
        label.grid(row=1, column=0, pady=(30, 10))

        label = Label(resultFrame, image=loadImage, text=self.player1Score, compound=CENTER, font=2.5, bg=self.background, fg="white")
        label.config(font=("Courier", 30))
        label.photo = loadImage
        label.grid(row=2, column=0)

        label = Label(resultFrame, image=loadp2WinnerImage, bg=self.background)
        label.photo = loadp2WinnerImage
        label.grid(row=1, column=2, pady=(30, 10))

        label = Label(resultFrame, image=loadImage, text=self.player2Score, compound=CENTER, font=2.5, bg=self.background, fg="white")
        label.config(font=("Courier", 30))
        label.photo = loadImage
        label.grid(row=2, column=2)

        submitBtn = Button(resultFrame, width=275, height=50, bd=-5, text='HOME', fg="white", bg="#b2854b", padx=0, pady=0, compound=CENTER, image=loadPlankImage, command=lambda: self.switchToMenu())
        submitBtn.config(font=("Courier", 20, "bold"))
        submitBtn.photo = loadPlankImage
        submitBtn.grid(row=8, column=1, pady=20)

        resultFrame.pack(side=TOP, expand=YES)
        gameOverFrame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

    def loadImage(self, image):
        return ImageTk.PhotoImage(image)

    def switchToMenu(self):
        self.controller.show_frame("MainPage")