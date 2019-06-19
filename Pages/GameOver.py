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

        if self.player2Name == "CPU":
            self.player2Name = "CPU Score"
        else:
            self.player2Name = "Player 2 Score"

        self.background = "#b2854b"
        image = Image.open("images/hole.png").resize((200, 200), Image.ANTIALIAS)
        loadImage = ImageTk.PhotoImage(image)

        gameOverFrame = Frame(self, bg=self.background)
        resultFrame = Frame(gameOverFrame, bg="#b2854b")

        label = Label(resultFrame, text="Game Over!", compound=CENTER, font=2.5, bg=self.background, fg="white")
        label.grid(row=0, columnspan=12, pady=15)

        label = Label(resultFrame, text="Player 1 Score", compound=CENTER, font=2.5, bg=self.background, fg="white")
        label.grid(row=1, column=0)

        label = Label(resultFrame, text="Results", compound=CENTER, font=2.5, bg=self.background, fg="white")
        label.grid(row=1, column=1)

        label = Label(resultFrame, image=loadImage, text=self.player1Score, compound=CENTER, font=2.5, bg=self.background, fg="white")
        label.config(font=("Courier", 44))
        label.photo = loadImage
        label.grid(row=2, column=0)

        label = Label(resultFrame, text=self.player2Name, compound=CENTER, font=2.5, bg=self.background, fg="white")
        label.grid(row=1, column=2)

        label = Label(resultFrame, image=loadImage, text=self.player2Score, compound=CENTER, font=2.5, bg=self.background, fg="white")
        label.config(font=("Courier", 44))
        label.photo = loadImage
        label.grid(row=2, column=2)

        submitBtn = Button(resultFrame, width=25, height=2, text='HOME', bd=5, bg="#ffffe0", command=lambda: self.switchToMenu())
        submitBtn.config(font=("Courier", 16, "bold"))
        submitBtn.grid(row=8, column=1, pady=40)

        resultFrame.pack(side=TOP, expand=YES)
        gameOverFrame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

    def switchToMenu(self):
        self.controller.show_frame("MainPage")