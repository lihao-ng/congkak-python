from tkinter import *
from Hole import Hole
from Player2 import Player

class Board:

    def __init__(self, holes, beads, player1, player2, frame):
        self.holes = holes
        self.beads = beads
        self.boardArray = []
        self.player1obj = player1
        self.p1name = self.player1obj.name
        self.player2obj = player2
        self.p2name = self.player2obj.name
        self.frame = frame
        self.p1side = "1st"
        self.p2side = "2nd"
        self.checkStatus = False
        self.haventWin = True
        self.indicator = 0
        self.extractscore = 0

    def init_holes(self):
        for index in range(0, self.holes):
            self.boardArray.append(Hole(self.beads, index))

    def left_click(self, iteration, cplayer):
        self.checkstatus(iteration, cplayer)

        if self.checkStatus == False:
            return
        else:
            if cplayer == self.p1name:
                cplayer = self.p2name
                self.player1obj.assignScore(self.extractscore)
                self.checkHaventWin(cplayer)
                if self.haventWin == False:
                    self.player1obj.assignRemaining(self.boardArray)
            elif cplayer == self.p2name:
                cplayer = self.p1name
                self.player2obj.assignScore(self.extractscore)
                self.checkHaventWin(cplayer)
                if self.haventWin == False:
                    self.player2obj.assignRemaining(self.boardArray)

            self.render_holes(self.indicator, cplayer)
            self.player1obj.render_player()
            self.player2obj.render_player()
            self.checkStatus = False

    def create_hole(self, hole, hole_counter, width, height, row, currentPlayer):
        label = Label(self.frame, text=hole.beads, borderwidth=6, relief="ridge", width=width, height=height, font=1.5)
        label.grid(row=row, column=hole_counter, padx=25, pady=25)
        label.bind("<Button-1>", lambda event, iteration=hole.iteration, cplayer=currentPlayer: self.left_click(iteration, cplayer))
        return label

    def render_holes(self, currentIndex, currentPlayer):
        hole_counter = 0
        width = 5
        height = 3

        for hole in self.boardArray[::-1]:
            if hole_counter < int((len(self.boardArray) / 2)):
                label = self.create_hole(hole, hole_counter, width, height, 1, currentPlayer)
                if hole.iteration == currentIndex:
                    label.configure(bg="orange")
                hole_counter += 1

        hole_counter = 0

        for hole in self.boardArray:
            if hole_counter < int((len(self.boardArray) / 2)):
                label = self.create_hole(hole, hole_counter, width, height, 2, currentPlayer)
                if hole.iteration == currentIndex:
                    label.configure(bg="orange")
                hole_counter += 1

    def chooseSide(self, side):
        if side == "y":
            self.p1side = "1st"
            self.p2side = "2nd"
        elif side == "n":
            self.p2side = "1st"
            self.p1side = "2nd"

    def evalBeads(self, index):
        self.nextIndex = index + 1

        if self.nextIndex < len(self.boardArray):
            if self.boardArray[self.nextIndex].beads != 0:
                self.calBeads(self.nextIndex)
            else:
                self.indicator = index
                self.extractScore(self.nextIndex)
        else:
            self.nextIndex -= len(self.boardArray)

            if self.boardArray[self.nextIndex].beads != 0:
                self.calBeads(self.nextIndex)
            else:
                self.indicator = index
                self.extractScore(self.nextIndex)

    def calBeads(self, index):
        self.move = self.boardArray[index].beads
        self.boardArray[index].beads = 0
        self.z = 1

        for i in range(self.move):
            self.newIndex = index + self.z
            if self.newIndex < len(self.boardArray):
                self.boardArray[self.newIndex].beads += 1
            else:
                self.newIndex -= len(self.boardArray)
                self.boardArray[self.newIndex].beads += 1
                self.z += 1
        index = self.newIndex
        self.evalBeads(index)

    def checkstatus(self, index, pname):
        if pname == self.p1name:
            if self.p1side == "1st":
                if index >= 0 and index < int(len(self.boardArray) / 2):
                    self.check1stRow()
                    if self.boardClear == False:
                        self.checkAmt(index)
                    else:
                        return
                else:
                    return
            else:
                if index >= int(len(self.boardArray) / 2) and index < len(self.boardArray):
                    self.check2ndRow()
                    if self.boardClear == False:
                        self.checkAmt(index)
                    else:
                        return
                else:
                    return
        else:
            if self.p2side == "1st":
                if index >= 0 and index < int(len(self.boardArray) / 2):
                    self.check1stRow()
                    if self.boardClear == False:
                        self.checkAmt(index)
                    else:
                        return
                else:
                    return
            else:
                if index >= int(len(self.boardArray) / 2) and index < len(self.boardArray):
                    self.check2ndRow()
                    if self.boardClear == False:
                        self.checkAmt(index)
                    else:
                        return
                else:
                    return

    def checkHaventWin(self, pname):
        if pname == self.p1name:
            if self.p1side == "1st":
                self.check1stRow()
                if self.boardClear: return
            else:
                self.check2ndRow()
                if self.boardClear: return
        else:
            if self.p2side == "1st":
                self.check1stRow()
                if self.boardClear: return
            else:
                self.check2ndRow()
                if self.boardClear: return

    def check1stRow(self):
        for i in range(0, int(len(self.boardArray) / 2)):
            if self.boardArray[i].beads != 0:
                self.boardClear = False
                self.haventWin = True
                return
            else:
                self.boardClear = True
                self.haventWin = False

    def check2ndRow(self):
        for i in range(int(len(self.boardArray) / 2), len(self.boardArray)):
            if self.boardArray[i].beads != 0:
                self.boardClear = False
                self.haventWin = True
                return
            else:
                self.boardClear = True
                self.haventWin = False

    def checkAmt(self, index):
        if self.boardArray[index].beads != 0:
            self.checkStatus = True
            self.calBeads(index)
        else:
            return

    def extractScore(self, index):
        self.newIndex = index + 1
        if self.newIndex < len(self.boardArray):
            self.extractscore = self.boardArray[self.newIndex].beads
            self.boardArray[self.newIndex].beads = 0
        else:
            self.newIndex -= len(self.boardArray)
            self.extractscore = self.boardArray[self.newIndex].beads
            self.boardArray[self.newIndex].beads = 0


