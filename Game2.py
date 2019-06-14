from tkinter import *
from Board2 import Board
from Player2 import Player
import time


class Game2(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        game_frame = Frame(self)
        board_frame = Frame(game_frame)
        player1_frame = Frame(game_frame, bg="aquamarine")
        player2_frame = Frame(game_frame, bg="orangered")

        game_frame.pack(side=TOP, expand=YES)
        player1_frame.grid(row=0, column=3, sticky=NSEW, padx=(10, 40))
        board_frame.grid(row=0, column=2)
        player2_frame.grid(row=0, column=1, sticky=NSEW, padx=(40, 10))

        # player2_frame.pack(side=RIGHT)
        # board_frame.pack(side=TOP, expand=YES)
        # player1_frame.pack(side=LEFT)

        player1 = Player("Lihao", player1_frame)
        player2 = Player("Jenson", player2_frame)
        board = Board(14, 4, board_frame)

        player1.render_player()
        player2.render_player()
        board.init_holes()
        board.render_holes()
