from tkinter import *
from PIL import Image, ImageTk
import time
from random import *
import globalValues
from Components.Hole import Hole
from Pages.GameOver import GameOver
from copy import *

INFINITY = 1.0e400

class AIBoard:

    def __init__(self, holes, beads, player1, player2, frame, controller):
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
        self.p1ABscore = 0
        self.p2ABscore = 0
        self.checkStatus = False
        self.haventWin = True
        self.indicator = 0
        self.extractscore = 0
        self.message = "Player 1's turn!"
        self.controller = controller
        self.playerMessage = Label(self.frame, text=self.message, compound=CENTER, font=1.5, bg="#4f3d21", fg="white")

    def init_holes(self):
        for index in range(0, self.holes):
            indicator = False
            if index < self.holes / 2:
                indicator = True
            self.boardArray.append(Hole(self.beads, index, indicator))

        self.playerMessage.grid(row=2, columnspan=int(len(self.boardArray)), pady=15)

    def left_click(self, iteration, cplayer):
        self.checkstatus(iteration, cplayer)

        if self.checkStatus == False:
            return
        else:
            if cplayer == self.p1name:
                cplayer = self.p2name
                self.render_message("Player 2's Turn!")
                self.player1obj.assignScore(self.extractscore)
                self.checkHaventWin(cplayer)
                if self.haventWin == False:
                    self.player1obj.assignRemaining(self.boardArray)
                    self.controller.show_frame("GameOver", className=GameOver, player1Score=self.player1obj.currentScore, player2Score=self.player2obj.currentScore, haveCpu=self.p2name)

                self.render_holes(self.indicator, cplayer)
                self.player1obj.render_player()
                self.player2obj.render_player()
                self.checkStatus = False

                if self.p2name == "CPU" and self.haventWin == True:
                    self.render_message("CPU's Turn!")
                    globalValues.screen.update()
                    time.sleep(1)
                    holeChosen = randint(len(self.boardArray) / 2, len(self.boardArray))
                    self.checkstatus(holeChosen, self.p2name)
                    cplayer = self.p1name
                    self.check_condition(cplayer)
                    self.render_message("Player 1's Turn!")

            elif cplayer == self.p2name:
                cplayer = self.p1name
                self.render_message("Player 1's Turn!")
                self.check_condition(cplayer)

            self.render_holes(self.indicator, cplayer)
            self.player1obj.render_player()
            self.player2obj.render_player()
            self.checkStatus = False

    def check_condition(self, cplayer):
        self.player2obj.assignScore(self.extractscore)
        self.checkHaventWin(cplayer)

        if self.haventWin == False:
            self.player2obj.assignRemaining(self.boardArray)
            self.controller.show_frame("GameOver", className=GameOver, player1Score=self.player1obj.currentScore, player2Score=self.player2obj.currentScore, haveCpu=self.p2name)

    def render_message(self, message):
        self.message = message
        self.playerMessage.configure(text=self.message)

    def create_hole(self, hole, hole_counter, row, currentPlayer):
        if hole.indicator == True and hole.beads != 0:
            image = Image.open("images/active-hole2.png").resize((135, 135), Image.ANTIALIAS)
        else:
            image = Image.open("images/hole2.png").resize((135, 135), Image.ANTIALIAS)

        loadImage = ImageTk.PhotoImage(image)
        label = Label(self.frame, image=loadImage, text=hole.beads, compound=CENTER, font=2.5, bg="#b2854b", fg="white")
        label.config(font=("Courier", 30))
        label.photo = loadImage
        label.grid(row=row, column=hole_counter)
        label.bind("<Button-1>", lambda event, iteration=hole.iteration, cplayer=currentPlayer: self.left_click(iteration, cplayer))
        return label

    def render_holes(self, currentIndex, currentPlayer):
        hole_counter = 0

        for hole in self.boardArray[::-1]:
            if hole_counter < int((len(self.boardArray) / 2)):
                label = self.create_hole(hole, hole_counter, 1, currentPlayer)
                hole_counter += 1

        hole_counter = 0
        self.render_message(self.message)

        for hole in self.boardArray:
            if hole_counter < int((len(self.boardArray) / 2)):
                label = self.create_hole(hole, hole_counter, 3, currentPlayer)
                hole_counter += 1

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
        self.newIndex = index

        for i in range(self.move):
            self.newIndex += 1
            if self.newIndex < len(self.boardArray):
                if self.move > 0:
                    self.boardArray[self.newIndex].beads += 1
                    self.move -= 1
            else:
                if self.move > 0:
                    self.newIndex = 0
                    self.boardArray[self.newIndex].beads += 1
                    self.move -= 1
        self.evalBeads(self.newIndex)

    def checkstatus(self, index, pname):
        if pname == self.p1name:
            self.changeP2Indicator()
            if index >= 0 and index < int(len(self.boardArray) / 2):
                self.check1stRow()
                if self.boardClear == False:
                    self.checkAmt(index)
                else:
                    return
            else:
                return
        else:
            self.changeP1Indicator()
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
            self.check1stRow()
            if self.boardClear:
                return
        else:
            self.check2ndRow()
            if self.boardClear:
                return

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

    def changeP1Indicator(self):
        for i in range(0, self.holes):
            if i < self.holes / 2:
                self.boardArray[i].indicator = True
            else:
                self.boardArray[i].indicator = False

    def changeP2Indicator(self):
        for i in range(0, self.holes):
            if i >= self.holes / 2:
                self.boardArray[i].indicator = True
            else:
                self.boardArray[i].indicator = False

    #AI stuff begins here

    def ABevalBeads(self, board, index, playerNum):
        ABnextIndex = index + 1

        if ABnextIndex < len(board):
            if board[ABnextIndex].beads != 0:
                self.ABcalBeads(board, ABnextIndex, playerNum)
            else:
                self.indicator = index
                self.ABextractScore(board, ABnextIndex, playerNum)
        else:
            ABnextIndex -= len(board)

            if board[ABnextIndex].beads != 0:
                self.ABcalBeads(board, ABnextIndex, playerNum)
            else:
                self.indicator = index
                self.ABextractScore(board, ABnextIndex, playerNum)

    def ABcalBeads(self, board, index, playerNum):
        ABmove = board[index].beads
        board[index].beads = 0
        ABnewIndex = index

        for i in range(ABmove):
            ABnewIndex += 1
            if ABnewIndex < len(board):
                if ABmove > 0:
                    board[ABnewIndex].beads += 1
                    ABmove -= 1
            else:
                if ABmove > 0:
                    ABnewIndex = 0
                    board[ABnewIndex].beads += 1
                    ABmove -= 1
        self.ABevalBeads(board, ABnewIndex, playerNum)

    def ABextractScore(self, board, index, playerNum):
        ABnewIndex = index + 1
        if ABnewIndex < len(board):
            if playerNum > 0:
                self.p1ABscore += board[ABnewIndex].beads
                board[ABnewIndex].beads = 0
            elif playerNum < 0:
                self.p2ABscore += board[ABnewIndex].beads
                board[ABnewIndex].beads = 0
        else:
            ABnewIndex -= len(board)
            if playerNum > 0:
                self.p1ABscore += board[ABnewIndex].beads
                board[ABnewIndex].beads = 0
            elif playerNum < 0:
                self.p2ABscore += board[ABnewIndex].beads
                board[ABnewIndex].beads = 0

    def ABgetScore(self, board, playerNum):
        if playerNum > 0:
            return board.p1ABscore
        elif playerNum < 0:
            return board.p2ABscore

    def checkAvailableMoves_ExtractIndex(self, board, playerNum):
        if playerNum > 0:
            self.branchingFactor = []
            for i in range(0, int(len(board) / 2)):
                if board[i].beads != 0:
                    self.branchingFactor.append(i)
        elif playerNum < 0:
            self.branchingFactor = []
            for i in range(int(len(board) / 2), len(board)):
                if board[i].beads != 0:
                    self.branchingFactor.append(i)
        return self.branchingFactor

    def AlphaBetaTrigger(self, board):
        self.alpha = -INFINITY
        self.beta = INFINITY
        self.boardCopy = deepcopy(board)
        self.playerNum = 1
        self.branches = self.checkAvailableMoves_ExtractIndex(self.boardCopy, self.playerNum)
        self.bestScore = -INFINITY

        for i in self.branches:
            self.score = max(self.alpha, self.MinAB(self.boardCopy, i, self.alpha, self.beta, self.playerNum))

            if self.score > self.bestScore:
                self.move = i
                self.bestScore = self.score

            self.alpha = max(self.alpha, self.score)
            self.p1ABscore = 0
            self.p2ABscore = 0
        return self.move, self.bestScore

    def MinAB(self, board, index, alpha, beta, playerNum):
        self.ABcalBeads(board, index, playerNum)
        playerNum *= -1
        boardCopy = deepcopy(board)
        branches = self.checkAvailableMoves_ExtractIndex(boardCopy, playerNum)

        for i in branches:
            score = min(beta, self.MaxAB(boardCopy, i, alpha, beta, playerNum))

            if score >= alpha:
                return score

            beta = min(beta, score)

        if board.haventWin == False:
            playerNum *= -1
            score = board.ABgetScore(board, playerNum)

        return score

    def MaxAB(self, board, index, alpha, beta, playerNum):
        self.ABcalBeads(board, index, playerNum)
        playerNum *= -1
        boardCopy = deepcopy(board)
        branches = self.checkAvailableMoves_ExtractIndex(boardCopy, playerNum)

        for i in branches:
            score = max(alpha, self.MinAB(boardCopy, i, alpha, beta, playerNum))

            if score < beta:
                return score

            alpha = max(alpha, score)

        if board.haventWin == False:
            playerNum *= -1
            score = board.ABgetScore(board, playerNum)

        return score


