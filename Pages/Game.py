from tkinter import *
from Components.Board import Board
from Components.Player import Player

class Game(Frame):

    def __init__(self, parent, controller, **kwargs):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#ffffe0")

        self.setValues(**kwargs)

        game_frame = Frame(self)
        board_frame = Frame(game_frame, bg="#4f3d21")
        player1_frame = Frame(game_frame, bg="#ffffe0")
        player2_frame = Frame(game_frame, bg="#ffffe0")

        game_frame.pack(side=TOP, expand=YES)
        player1_frame.grid(row=0, column=1, sticky=NSEW)
        board_frame.grid(row=0, column=2, sticky=NSEW)
        player2_frame.grid(row=0, column=3, sticky=NSEW)

        player1 = Player("Player_1", player1_frame)
        player2 = Player(self.secondPlayer, player2_frame)
        board = Board(self.holes, self.beads, player1, player2, board_frame, controller)

        player1.render_player()
        player2.render_player()
        board.init_holes()
        board.render_holes(0, player1.name)

    def setValues(self, **kwargs):
        holes = kwargs.get("holes")
        beads = kwargs.get("beads")
        haveCPU = kwargs.get("haveCPU")

        if holes:
            self.holes = int(holes)
        else:
            self.holes = 14

        if beads:
            self.beads = int(beads)
        else:
            self.beads = 4

        if haveCPU:
            if haveCPU == "CPU":
                self.secondPlayer = "CPU"
            else:
                self.secondPlayer = "Player_2"
        else:
            self.secondPlayer = "CPU"