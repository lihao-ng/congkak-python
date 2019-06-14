from tkinter import *
from Hole import Hole


class Board:
    holes = []

    def __init__(self, num_of_holes, beads, frame):
        self.num_of_holes = num_of_holes
        self.beads = beads
        self.frame = frame

    def init_holes(self):
        for index in range(0, self.num_of_holes):
            self.holes.append(Hole(self.beads, index))

    def left_click(self, iteration):
        print(iteration)

    def create_hole(self, hole, hole_counter, width, height, row):
        label = Label(self.frame, text=hole.beads, borderwidth=6, relief="ridge", width=width, height=height, font=1.5)
        label.grid(row=row, column=hole_counter, padx=25, pady=25)
        label.bind("<Button-1>", lambda event, iteration=hole.iteration: self.left_click(iteration))
        return label

    def render_holes(self):
        hole_counter = 0
        width = 5
        height = 3

        for hole in self.holes[::-1]:
            if hole_counter < 7:
                label = self.create_hole(hole, hole_counter, width, height, 1)
                if hole.iteration == 9:
                    label.configure(bg="orange")
                hole_counter += 1

        hole_counter = 0

        for hole in self.holes:
            if hole_counter < 7:
                label = self.create_hole(hole, hole_counter, width, height, 2)
                if hole.iteration == 9:
                    label.configure(bg="orange")
                hole_counter += 1
