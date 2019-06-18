import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
from SelectMode import SelectMode
from PIL import ImageTk, Image

class Page(tk.Tk):
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
        for F in (MainPage, SelectMode):
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
        label.pack(pady=50)

        mainMenuBtn = tk.Button(self,width=25, height=2, text='START GAME', bd=5, bg="red",
                            command=lambda: controller.show_frame("SelectMode"))
        mainMenuBtn.pack(pady=20)


app = Page()
app.mainloop()