from tkinter import *
from tkinter import font

from PIL import ImageTk, Image

from Pages.SelectMode import SelectMode
import globalValues

global tk

class Main(Tk):
    def __init__(self, *args, **kwargs):

        Tk.__init__(self, *args, **kwargs)
        globalValues.screen = self
        self.title("Mangala")
        self.title_font = font.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        # self.configure(bg="white")
        self.state('zoomed')

        self.pages = (MainPage, SelectMode)
        self.container = Frame(self)
        self.container.pack(side="top", fill=BOTH, expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        page_name = MainPage.__name__
        frame = MainPage(self.container, self)
        self.frames[page_name] = frame
        frame.grid(row=0, column=0, sticky=NSEW)

        self.show_frame("MainPage")

    def show_frame(self, page_name, **kwargs):
        if page_name not in self.frames:
            # self.frames[page_name] = frame
            className = kwargs.get("className")
            frame = className(self.container, self, **kwargs)
            frame.grid(row=0, column=0, sticky=NSEW)
        else:
            frame = self.frames[page_name]
        frame.tkraise()

class MainPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.background = "#ffffe0"
        self.configure(bg=self.background)

        menuFrame = Frame(self, bg=self.background)
        img = ImageTk.PhotoImage(Image.open("images/congkakGameLogo.png"))
        label = Label(menuFrame, image=img, bg=self.background)
        label.image = img
        label.pack(pady=50)

        mainMenuBtn = Button(menuFrame, width=25, height=2, text='START GAME', bd=5, bg="#b2854b", command=lambda: controller.show_frame("SelectMode", className=SelectMode))
        mainMenuBtn.config(font=("Courier", 16, "bold"))
        mainMenuBtn.pack(pady=10)
        menuFrame.pack(side=TOP, expand=YES)

app = Main()
app.mainloop()
