import tkinter as tk
from tkinter import *
from tkinter import messagebox

class SelectMode(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="white")

        btnDefaultColor = "orange"
        btnSelectedColor = "white"
        self.gameMode = ""
        self.opponentType = ""
        self.holesDefault = IntVar()
        self.beadsDefault = IntVar()


        label1 = tk.Label(self, text="Select Mode:", font=controller.title_font, bg="white")
        label1.grid(row=0,padx=20,pady=20)

        normalModeBtn=tk.Button(self, width=25, height=2, text='NORMAL', bd=5, bg=btnDefaultColor, command=lambda: selectMode('normal'))
        normalModeBtn.grid(row=1, column=0)

        intermediateModeBtn = tk.Button(self, width=25, height=2, text='INTERMEDIATE', bd=5, bg=btnDefaultColor, command=lambda: selectMode('intermediate'))
        intermediateModeBtn.grid(row=1, column=1, padx=40)

        advancedModeBtn = tk.Button(self, width=25, height=2, text='ADVANCED', bd=5, bg=btnDefaultColor, command=lambda: selectMode('hard'))
        advancedModeBtn.grid(row=1, column=2,padx=40)

        label1 = tk.Label(self, text="Select Opponent:", font=controller.title_font, bg="white")
        label1.grid(row=2,padx=20,pady=20)

        player2Btn=tk.Button(self, width=25, height=2, text='PLAYER 2', bd=5, bg=btnDefaultColor, command=lambda: selectOpponent('player2'))
        player2Btn.grid(row=3, column=0)

        CPUbtn = tk.Button(self, width=25, height=2, text='CPU', bd=5, bg=btnDefaultColor, command=lambda: selectOpponent('ui'))
        CPUbtn.grid(row=3, column=1, padx=40)

        labelBeads = tk.Label(self, text="Number Of Bead:", font=controller.title_font,  bg="white")
        labelBeads.grid(row=4, column=0, pady=20)

        self.numOfBeads = tk.Entry(self, width=25, bd=5, bg=btnDefaultColor, textvariable= self.beadsDefault)
        self.beadsDefault.set(4)
        self.numOfBeads.grid(row=5, column=0)

        labelHoles = tk.Label(self, text="Number Of Holes:", font=controller.title_font,  bg="white")
        labelHoles.grid(row=4, column=1, pady=20)

        self.numOfHoles = tk.Entry(self, width=25, bd=5, bg=btnDefaultColor, textvariable= self.holesDefault)
        self.holesDefault.set(14)
        self.numOfHoles.grid(row=5, column=1)

        submitBtn = tk.Button(self, width=25, height=2, text='START GAME', bd=5, bg="red", command=lambda: checkUserInput())
        submitBtn.grid(row=8, column=1, pady=40)


        def checkUserInput():
            if(self.gameMode == ""):
                messagebox.showerror("Error", "Please select Mode")
            elif(self.opponentType == ""):
                messagebox.showerror("Error", "Please select Opponent")
            elif (int(self.numOfHoles.get()) % 2 != 0):
                messagebox.showerror("Error", "Number of Holes have to be Even Number")
            else:
                 controller.show_frame("MainPage");



        def selectMode(mode):
            if mode == "normal":
                self.beadsDefault.set(4)
                self.holesDefault.set(14)
                normalModeBtn.configure(bg=btnSelectedColor, text="NORMAL SELECTED!")
                intermediateModeBtn.configure(bg=btnDefaultColor, text="INTERMEDIATE")
                advancedModeBtn.configure(bg=btnDefaultColor, text="ADVANCED")
                labelBeads.grid_forget()
                self.numOfBeads.grid_forget()
                labelHoles.grid_forget()
                self.numOfHoles.grid_forget()

            elif mode == "intermediate":
                self.gameMode = "intermediate"
                intermediateModeBtn.configure(bg=btnSelectedColor, text="INTERMEDIATE SELECTED!")
                normalModeBtn.configure(bg=btnDefaultColor, text="NORMAL")
                advancedModeBtn.configure(bg=btnDefaultColor, text="ADVANCED")
                labelBeads.grid(row=4, column=0, pady=20)
                self.numOfBeads.grid(row=5, column=0)
                labelHoles.grid(row=4, column=1, pady=20)
                self.numOfHoles.grid(row=5, column=1)

            elif mode == "hard":
                self.gameMode = "hard"
                advancedModeBtn.configure(bg=btnSelectedColor, text="ADVANCED SELECTED!")
                normalModeBtn.configure(bg=btnDefaultColor, text="NORMAL")
                intermediateModeBtn.configure(bg=btnDefaultColor, text="INTERMEDIATE")
                labelBeads.grid(row=4, column=0, pady=20)
                self.numOfBeads.grid(row=5, column=0)
                labelHoles.grid(row=4, column=1, pady=20)
                self.numOfHoles.grid(row=5, column=1)


        def selectOpponent(opponent):
            if opponent == "player2":
                self.opponentType = "player2"
                player2Btn.configure(bg=btnSelectedColor, text="PLAYER 2 SELECTED!")
                CPUbtn.configure(bg=btnDefaultColor, text="UI")

            elif opponent == "ui":
                self.opponentType = "ui"
                CPUbtn.configure(bg=btnSelectedColor, text="UI SELECTED!")
                player2Btn.configure(bg=btnDefaultColor, text="PLAYER 2")