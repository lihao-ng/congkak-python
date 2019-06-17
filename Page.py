import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
from PIL import ImageTk,Image

class page(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Mangala")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.configure(bg="white")

        container = tk.Frame(width=1200, height=800)
        container.pack(side="top", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainPage, PageOne):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="white")
        img = ImageTk.PhotoImage(Image.open("img/congkakGameLogo.png"))
        label = Label(self, image =img, bg="white")
        label.image = img
        label.pack(pady=90)

        mainMenuBtn = tk.Button(self,width=25, height=2, text='START GAME', bd=5, bg="red",
                            command=lambda: controller.show_frame("PageOne"))
        mainMenuBtn.pack(pady=20)



class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="white")

        btnDefaultColor = "orange"
        btnSelectedColor = "white"
        numOfBeads = IntVar()
        numOfHoles = IntVar()
        gameMode = StringVar()
        opponentType = StringVar()

        def selectMode(mode):
            if mode == "normal":
                gameMode = "normal"
                normalModeBtn.configure(bg=btnSelectedColor, text="NORMAL SELECTED!")
                intermediateModeBtn.configure(bg=btnDefaultColor, text="INTERMEDIATE")
                advancedModeBtn.configure(bg=btnDefaultColor, text="ADVANCED")

            elif mode == "intermediate":
                gameMode = "intermediate"
                intermediateModeBtn.configure(bg=btnSelectedColor, text="INTERMEDIATE SELECTED!")
                normalModeBtn.configure(bg=btnDefaultColor, text="NORMAL")
                advancedModeBtn.configure(bg=btnDefaultColor, text="ADVANCED")

            elif mode == "hard":
                gameMode = "hard"
                advancedModeBtn.configure(bg=btnSelectedColor, text="ADVANCED SELECTED!")
                normalModeBtn.configure(bg=btnDefaultColor, text="NORMAL")
                intermediateModeBtn.configure(bg=btnDefaultColor, text="INTERMEDIATE")

        def selectOpponent(opponent):
            if opponent == "player2":
                opponentType = "player2"
                player2Btn.configure(bg=btnSelectedColor, text="PLAYER 2 SELECTED!")
                UIbtn.configure(bg=btnDefaultColor, text="UI")

            elif opponent == "ui":
                opponentType = "ui"
                UIbtn.configure(bg=btnSelectedColor, text="UI SELECTED!")
                player2Btn.configure(bg=btnDefaultColor, text="PLAYER 2")


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

        UIbtn = tk.Button(self, width=25, height=2, text='UI', bd=5, bg=btnDefaultColor, command=lambda: selectOpponent('ui'))
        UIbtn.grid(row=3, column=1, padx=40)

        label2 = tk.Label(self, text="Number Of Bead:", font=controller.title_font,  bg="white")
        label2.grid(row=4, column=0, pady=20)

        btn = tk.Entry(self, width=25, text='ADVANCED', bd=5, bg=btnDefaultColor, textvariable=numOfBeads)
        btn.grid(row=5, column=0)

        label2 = tk.Label(self, text="Number Of Hole:", font=controller.title_font,  bg="white")
        label2.grid(row=6, column=0, pady=20)

        btn = tk.Entry(self, width=25, text='ADVANCED', bd=5, bg=btnDefaultColor, textvariable=numOfHoles)
        btn.grid(row=7, column=0)

        submitBtn = tk.Button(self,width=25, height=2, text='START GAME', bd=5, bg="red")
        submitBtn.grid(row=8, column=1, pady=40)





app = page()
app.mainloop()