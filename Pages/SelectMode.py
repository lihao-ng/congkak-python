from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk
from Pages.Game import Game

class SelectMode(Frame):

    def __init__(self, parent, controller, **kwargs):
        Frame.__init__(self, parent)
        self.controller = controller

        self.background = "#b2854b"
        self.color = "white"
        self.btnDefaultColor = "#ffffe0"
        self.btnSelectedColor = "#4f3d21"

        self.configure(bg=self.btnDefaultColor)
        self.gameMode = ""
        self.opponentType = ""
        self.holesDefault = IntVar()
        self.beadsDefault = IntVar()

        image = Image.open("images/plank.png").resize((275, 50), Image.ANTIALIAS)
        loadImage = ImageTk.PhotoImage(image)

        outerFrame = Frame(self, bg=self.background)
        selectModeFrame = Frame(outerFrame, bg=self.background)

        label1 = Label(selectModeFrame, text="Select Mode:", font=controller.title_font, bg=self.background, fg=self.color)
        label1.config(font=("Courier", 18, "bold"))
        label1.grid(row=0, column=0, padx=20, pady=20)

        normalModeBtn= Button(selectModeFrame, width=275, height=50, bd=-5, fg="white", bg=self.btnSelectedColor, text='NORMAL', image=loadImage, padx=0, pady=0, compound=CENTER, command=lambda: selectMode('normal'))
        normalModeBtn.config(font=("Courier", 14, "bold"))
        normalModeBtn.image = loadImage
        normalModeBtn.grid(row=1, column=0, pady=20)

        intermediateModeBtn = Button(selectModeFrame, width=275, height=50, bd=-5, fg="white", bg=self.btnSelectedColor, text='INTERMEDIATE', image=loadImage, padx=0, pady=0, compound=CENTER, command=lambda: selectMode('intermediate'))
        intermediateModeBtn.config(font=("Courier", 14, "bold"))
        intermediateModeBtn.image = loadImage
        intermediateModeBtn.grid(row=1, column=1, padx=20)

        advancedModeBtn = Button(selectModeFrame, width=275, height=50, bd=-5, fg="white", bg=self.btnSelectedColor, text='ADVANCED', image=loadImage, padx=0, pady=0, compound=CENTER, command=lambda: selectMode('hard'))
        advancedModeBtn.config(font=("Courier", 14, "bold"))
        advancedModeBtn.image = loadImage
        advancedModeBtn.grid(row=1, column=2,padx=20)

        label1 = Label(selectModeFrame, text="Select Opponent:", font=controller.title_font, bg=self.background, fg=self.color)
        label1.config(font=("Courier", 18, "bold"))
        label1.grid(row=2,padx=20,pady=20)

        player2Btn = Button(selectModeFrame, width=275, height=50, bd=-5, fg="white", bg=self.btnSelectedColor, text='PLAYER 2', image=loadImage, padx=0, pady=0, compound=CENTER, command=lambda: selectOpponent('Player_2'))
        player2Btn.config(font=("Courier", 14, "bold"))
        player2Btn.image = loadImage
        player2Btn.grid(row=3, column=0, padx=20)

        CPUbtn = Button(selectModeFrame, width=275, height=50, bd=-5, fg="white", bg=self.btnSelectedColor, text='CPU', image=loadImage, padx=0, pady=0, compound=CENTER, command=lambda: selectOpponent('CPU'))
        CPUbtn.config(font=("Courier", 14, "bold"))
        CPUbtn.image = loadImage
        CPUbtn.grid(row=3, column=1, padx=20)

        labelBeads = Label(selectModeFrame, text="Number Of Beads:", font=controller.title_font, bg=self.background, fg=self.color)
        labelBeads.config(font=("Courier", 18, "bold"))
        labelBeads.grid(row=4, column=0, pady=20)

        self.numOfBeads = Entry(selectModeFrame, width=25, bd=5, bg=self.btnDefaultColor, textvariable= self.beadsDefault)
        self.numOfBeads.config(font=("Courier", 14, "bold"))
        self.beadsDefault.set(4)
        self.numOfBeads.grid(row=5, column=0)

        labelHoles = Label(selectModeFrame, text="Number Of Holes:", font=controller.title_font, bg=self.background, fg=self.color)
        labelHoles.config(font=("Courier", 18, "bold"))
        labelHoles.grid(row=4, column=1, pady=20)

        self.numOfHoles = Entry(selectModeFrame, width=25, bd=5, bg=self.btnDefaultColor, textvariable= self.holesDefault)
        self.numOfHoles.config(font=("Courier", 14, "bold"))
        self.holesDefault.set(14)
        self.numOfHoles.grid(row=5, column=1)

        submitBtn = Button(selectModeFrame, width=275, height=50, bd=-5, fg="white", bg=self.btnSelectedColor, text='START GAME', image=loadImage, padx=0, pady=0, compound=CENTER, command=lambda: checkUserInput())
        submitBtn.config(font=("Courier", 20, "bold"))
        submitBtn.photo = loadImage
        submitBtn.grid(row=8, column=1, pady=40)

        selectModeFrame.pack(side=TOP, expand=YES)
        outerFrame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        def checkUserInput():
            if self.gameMode == "":
                messagebox.showerror("Error", "Please select Mode")
            elif self.opponentType == "":
                messagebox.showerror("Error", "Please select Opponent")
            elif int(self.numOfHoles.get()) % 2 != 0 or int(self.numOfHoles.get()) == 0:
                messagebox.showerror("Error", "Number of Holes have to be Even Number ")
            elif int(self.numOfHoles.get()) <= 2:
                messagebox.showerror("Error", "Number of Holes cannot be lesser than 2")
            elif int(self.numOfHoles.get()) > 20:
                messagebox.showerror("Error", "Number of Holes cannot be more than 20")
            elif int(self.numOfBeads.get()) == 0:
                messagebox.showerror("Error", "Number of Beads cannot be 0")
            else:
                self.controller.show_frame("Game", className=Game, holes=self.numOfHoles.get(), beads=self.numOfBeads.get(), haveCPU=self.opponentType, gameMode=self.gameMode)


        def selectMode(mode):
            if mode == "normal":
                self.beadsDefault.set(4)
                self.holesDefault.set(14)
                self.gameMode = "normal"
                normalModeBtn.configure(text="NORMAL SELECTED!")
                intermediateModeBtn.configure( text="INTERMEDIATE")
                advancedModeBtn.configure(text="ADVANCED")
                labelBeads.grid_forget()
                self.numOfBeads.grid_forget()
                labelHoles.grid_forget()
                self.numOfHoles.grid_forget()

            elif mode == "intermediate":
                self.gameMode = "intermediate"
                intermediateModeBtn.configure(text="INTERMEDIATE SELECTED!")
                normalModeBtn.configure( text="NORMAL")
                advancedModeBtn.configure(text="ADVANCED")
                labelBeads.grid(row=4, column=0, pady=20)
                self.numOfBeads.grid(row=5, column=0)
                labelHoles.grid(row=4, column=1, pady=20)
                self.numOfHoles.grid(row=5, column=1)

            elif mode == "hard":
                self.gameMode = "hard"
                advancedModeBtn.configure(text="ADVANCED SELECTED!")
                normalModeBtn.configure(text="NORMAL")
                intermediateModeBtn.configure(text="INTERMEDIATE")
                labelBeads.grid(row=4, column=0, pady=20)
                self.numOfBeads.grid(row=5, column=0)
                labelHoles.grid(row=4, column=1, pady=20)
                self.numOfHoles.grid(row=5, column=1)


        def selectOpponent(opponent):
            if opponent == "Player_2":
                self.opponentType = "Player_2"
                player2Btn.configure(text="PLAYER 2 SELECTED!")
                CPUbtn.configure(text="CPU")

            elif opponent == "CPU":
                self.opponentType = "CPU"
                CPUbtn.configure(text="CPU SELECTED!")
                player2Btn.configure(text="PLAYER 2")