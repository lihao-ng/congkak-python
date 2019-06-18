from tkinter import *
from tkinter import font

from PIL import ImageTk, Image

from Pages.GameOver import GameOver
from Pages.SelectMode import SelectMode

class Main(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title("Mangala")
        self.title_font = font.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.configure(bg="white")
        self.pages = (MainPage, SelectMode, GameOver)

        self.container = Frame(self, width=1200, height=800)
        self.container.pack(side="top", fill=BOTH, expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in self.pages:
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky=NSEW)

        self.show_frame(MainPage)

    def show_frame(self, page_name, **kwargs):
        if page_name not in self.frames:
            frame = page_name(self.container, self, **kwargs)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky=NSEW)

        frame = self.frames[page_name]
        frame.tkraise()

class MainPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="white")
        img = ImageTk.PhotoImage(Image.open("images/congkakGameLogo.png"))
        label = Label(self, image=img, bg="white")
        label.image = img
        label.pack(pady=50)

        mainMenuBtn = Button(self,width=25, height=2, text='START GAME', bd=5, bg="red",
                            command=lambda: controller.show_frame(SelectMode))
        mainMenuBtn.pack(pady=20)


app = Main()
app.mainloop()
