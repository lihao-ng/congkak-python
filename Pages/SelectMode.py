from tkinter import *
from tkinter import messagebox

from Pages.Game import Game

class SelectMode(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="white")
        self.btnDefaultColor = "orange"
        self.btnSelectedColor = "white"
        self.gameMode = ""
        self.opponentType = ""
        self.holesDefault = IntVar()
        self.beadsDefault = IntVar()


        label1 = Label(self, text="Select Mode:", font=controller.title_font, bg="white")
        label1.grid(row=0,padx=20,pady=20)

        normalModeBtn= Button(self, width=25, height=2, text='NORMAL', bd=5, bg=self.btnDefaultColor, command=lambda: selectMode('normal'))
        normalModeBtn.grid(row=1, column=0)

        intermediateModeBtn = Button(self, width=25, height=2, text='INTERMEDIATE', bd=5, bg=self.btnDefaultColor, command=lambda: selectMode('intermediate'))
        intermediateModeBtn.grid(row=1, column=1, padx=40)

        advancedModeBtn = Button(self, width=25, height=2, text='ADVANCED', bd=5, bg=self.btnDefaultColor, command=lambda: selectMode('hard'))
        advancedModeBtn.grid(row=1, column=2,padx=40)

        label1 = Label(self, text="Select Opponent:", font=controller.title_font, bg="white")
        label1.grid(row=2,padx=20,pady=20)

        player2Btn= Button(self, width=25, height=2, text='PLAYER 2', bd=5, bg=self.btnDefaultColor, command=lambda: selectOpponent('Player_2'))
        player2Btn.grid(row=3, column=0)

        CPUbtn = Button(self, width=25, height=2, text='CPU', bd=5, bg=self.btnDefaultColor, command=lambda: selectOpponent('CPU'))
        CPUbtn.grid(row=3, column=1, padx=40)

        labelBeads = Label(self, text="Number Of Bead:", font=controller.title_font,  bg="white")
        labelBeads.grid(row=4, column=0, pady=20)

        self.numOfBeads = Entry(self, width=25, bd=5, bg=self.btnDefaultColor, textvariable= self.beadsDefault)
        self.beadsDefault.set(4)
        self.numOfBeads.grid(row=5, column=0)

        labelHoles = Label(self, text="Number Of Holes:", font=controller.title_font,  bg="white")
        labelHoles.grid(row=4, column=1, pady=20)

        self.numOfHoles = Entry(self, width=25, bd=5, bg=self.btnDefaultColor, textvariable= self.holesDefault)
        self.holesDefault.set(14)
        self.numOfHoles.grid(row=5, column=1)

        submitBtn = Button(self, width=25, height=2, text='START GAME', bd=5, bg="red", command=lambda: checkUserInput())
        submitBtn.grid(row=8, column=1, pady=40)


        def checkUserInput():
            if self.gameMode == "":
                messagebox.showerror("Error", "Please select Mode")
            elif self.opponentType == "":
                messagebox.showerror("Error", "Please select Opponent")
            elif int(self.numOfHoles.get()) % 2 != 0 or int(self.numOfHoles.get()) == 0:
                messagebox.showerror("Error", "Number of Holes have to be Even Number ")
            elif int(self.numOfBeads.get()) == 0:
                messagebox.showerror("Error", "Number of Beads cannot be 0")
            else:
                self.controller.show_frame(Game, holes=self.numOfHoles.get(), beads=self.numOfBeads.get(), haveCPU=self.opponentType)


        def selectMode(mode):
            if mode == "normal":
                self.beadsDefault.set(4)
                self.holesDefault.set(14)
                self.gameMode = "normal"
                normalModeBtn.configure(bg=self.btnSelectedColor, text="NORMAL SELECTED!")
                intermediateModeBtn.configure(bg=self.btnDefaultColor, text="INTERMEDIATE")
                advancedModeBtn.configure(bg=self.btnDefaultColor, text="ADVANCED")
                labelBeads.grid_forget()
                self.numOfBeads.grid_forget()
                labelHoles.grid_forget()
                self.numOfHoles.grid_forget()

            elif mode == "intermediate":
                self.gameMode = "intermediate"
                intermediateModeBtn.configure(bg=self.btnSelectedColor, text="INTERMEDIATE SELECTED!")
                normalModeBtn.configure(bg=self.btnDefaultColor, text="NORMAL")
                advancedModeBtn.configure(bg=self.btnDefaultColor, text="ADVANCED")
                labelBeads.grid(row=4, column=0, pady=20)
                self.numOfBeads.grid(row=5, column=0)
                labelHoles.grid(row=4, column=1, pady=20)
                self.numOfHoles.grid(row=5, column=1)

            elif mode == "hard":
                self.gameMode = "hard"
                advancedModeBtn.configure(bg=self.btnSelectedColor, text="ADVANCED SELECTED!")
                normalModeBtn.configure(bg=self.btnDefaultColor, text="NORMAL")
                intermediateModeBtn.configure(bg=self.btnDefaultColor, text="INTERMEDIATE")
                labelBeads.grid(row=4, column=0, pady=20)
                self.numOfBeads.grid(row=5, column=0)
                labelHoles.grid(row=4, column=1, pady=20)
                self.numOfHoles.grid(row=5, column=1)


        def selectOpponent(opponent):
            if opponent == "Player_2":
                self.opponentType = "Player_2"
                player2Btn.configure(bg=self.btnSelectedColor, text="PLAYER 2 SELECTED!")
                CPUbtn.configure(bg=self.btnDefaultColor, text="CPU")

            elif opponent == "CPU":
                self.opponentType = "CPU"
                CPUbtn.configure(bg=self.btnSelectedColor, text="CPU SELECTED!")
                player2Btn.configure(bg=self.btnDefaultColor, text="PLAYER 2")