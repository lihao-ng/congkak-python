from tkinter import *
from PIL import Image, ImageTk
import time
from random import *
import globalValues
from Components.Hole import Hole
from Pages.GameOver import GameOver
import copy

from sys import *

sys.setrecursionlimit(8000)
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
        self.ABhaventWin = True
        self.indicator = 0
        self.extractscore = 0
        self.message = "Player 1's turn!"
        self.controller = controller
        self.playerMessage = Label(self.frame, text=self.message, compound=CENTER, font=1.5, bg="#4f3d21", fg="white")
        self.AIBtn = Label(self.frame, text='TEST AI', bg="#b2854b")

    def init_holes(self):
        for index in range(0, self.holes):
            indicator = False
            if index < self.holes / 2:
                indicator = True
            self.boardArray.append(Hole(self.beads, index, indicator))

        self.playerMessage.grid(row=2, columnspan=int(len(self.boardArray)), pady=15)
        self.AIBtn.grid(row=5, column=0, pady=15)
        self.AIBtn.bind("<Button-1>", lambda event, a=self.boardArray: self.AlphaBetaTrigger(a))

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
                self.ABextractScore(board, ABnextIndex, playerNum)
                if playerNum > 0:
                    self.ABcheck1stRow(board)
                elif playerNum < 0:
                    self.ABcheck2ndRow(board)
                if self.ABhaventWin == False:
                    self.ABassignRemaining(board, playerNum)
        else:
            ABnextIndex -= len(board)

            if board[ABnextIndex].beads != 0:
                self.ABcalBeads(board, ABnextIndex, playerNum)
            else:
                self.ABextractScore(board, ABnextIndex, playerNum)
                if playerNum > 0:
                    self.ABcheck1stRow(board)
                elif playerNum < 0:
                    self.ABcheck2ndRow(board)
                if self.ABhaventWin == False:
                    self.ABassignRemaining(board, playerNum)

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

    def ABassignRemaining(self, board, playerNum):
        if playerNum > 0:
            for i in board:
                self.p2ABscore += i.beads
                i.beads = 0
        elif playerNum < 0:
            for i in board:
                self.p1ABscore += i.beads
                i.beads = 0

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
            return self.p1ABscore
        elif playerNum < 0:
            return self.p2ABscore

    def ABcheck1stRow(self, board):
        for i in range(0, int(len(board) / 2)):
            if board[i].beads != 0:
                self.ABhaventWin = True
                return
            else:
                self.ABhaventWin = False

    def ABcheck2ndRow(self, board):
        for i in range(int(len(board) / 2), len(board)):
            if board[i].beads != 0:
                self.ABhaventWin = True
                return
            else:
                self.ABhaventWin = False

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
        self.boardCopy = copy.deepcopy(board)
        self.playerNum = 1
        self.branches = self.checkAvailableMoves_ExtractIndex(self.boardCopy, self.playerNum)
        self.bestScore = -INFINITY
        self.ABcounter = 0
        print("branches at depth trigger "+str(self.ABcounter)+" is "+str(self.branches))

        for i in self.branches:
            print("branches at depth trigger "+str(self.ABcounter)+" is "+str(self.branches)+" with value of i="+str(i))
            self.score = max(self.alpha, self.MinAB(self.boardCopy, i, self.playerNum))
            print(str(self.score)+" is the value of score at trigger & beta & alpha"+str(self.beta)+str(self.alpha))
            if self.score > self.bestScore:
                self.move = i
                self.bestScore = self.score

            self.alpha = max(self.alpha, self.score)
            self.p1ABscore = 0
            self.p2ABscore = 0
            self.ABhaventWin = True
        print("Value of move is "+str(self.move)+" and the value of bestScore is "+str(self.bestScore))
        #return self.move, self.bestScore

    def MinAB(self, board, index, playerNum):
        self.ABcalBeads(board, index, playerNum)
        playerNum = -1
        boardCopy = copy.deepcopy(board)
        branches = self.checkAvailableMoves_ExtractIndex(boardCopy, playerNum)
        score = INFINITY
        print("branches at depth "+str(self.ABcounter)+" in MinAB is "+str(branches))

        for i in branches:
            score = min(score, self.MaxAB(boardCopy, i, playerNum))
            print(str(score)+" is the value of score")
            print("The value of beta is "+str(self.beta)+"at depth "+str(self.ABcounter))

            self.beta = min(self.beta, score)
            print(str(self.beta)+" is the value of beta")
            if score > self.alpha:
                print("pruned at MinAB")
                return score
            return score

        if len(branches) == 0:
            if self.ABhaventWin == False:
                playerNum = 1
                score = min(score, self.ABgetScore(board, playerNum))
                self.alpha = max(self.alpha, score)
                print("game ends here\n")
        self.ABcounter += 1
        return score

    def MaxAB(self, board, index, playerNum):
        self.ABcalBeads(board, index, playerNum)
        playerNum = 1
        boardCopy = copy.deepcopy(board)
        branches = self.checkAvailableMoves_ExtractIndex(boardCopy, playerNum)
        score = -INFINITY
        print("branches at depth "+str(self.ABcounter)+" in MaxAB is "+str(branches))
        for i in branches:
            score = max(score, self.MinAB(boardCopy, i, playerNum))
            print(str(score)+" is the value of score")
            print("The value of alpha is "+str(self.alpha)+"at depth "+str(self.ABcounter))

            self.alpha = max(self.alpha, score)
            print(str(self.alpha)+" is the value of alpha")
            if score < self.beta:
                print("pruned at MaxAB")
                return score
            return score

        if len(branches) == 0:
            if self.ABhaventWin == False:
                playerNum = -1
                score = max(score, self.ABgetScore(board, playerNum))
                self.beta = min(self.beta, score)
                print("game ends here\n")
        self.ABcounter += 1
        return score


