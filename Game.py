from tkinter import *
from Board import Board
from Player import Player

class Game(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        game_frame = Frame(self)
        board_frame = Frame(game_frame, bg="#4f3d21")
        player1_frame = Frame(game_frame)
        player2_frame = Frame(game_frame)

        game_frame.pack(side=TOP, expand=YES)
        player1_frame.grid(row=0, column=1, sticky=NSEW)
        board_frame.grid(row=0, column=2, sticky=NSEW)
        player2_frame.grid(row=0, column=3, sticky=NSEW)

        player1 = Player("Player_1", player1_frame)
        player2 = Player("Player_2", player2_frame)
        board = Board(6, 2, player1, player2, board_frame, controller)

        player1.render_player()
        player2.render_player()
        board.init_holes()
        board.render_holes(0, player1.name)
