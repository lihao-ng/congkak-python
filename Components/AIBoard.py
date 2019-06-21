from tkinter import *
from PIL import Image, ImageTk
import time
from random import *
import globalValues
from Components.Hole import Hole
from Pages.GameOver import GameOver
from tkinter import messagebox
import copy

from sys import *

sys.setrecursionlimit(2000)
INFINITY = 1.0e400

class AIBoard:

    def __init__(self, holes, beads, player1, player2, frame, controller, parent):
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
        self.ABroundScore = 0
        self.checkStatus = False
        self.haventWin = True
        self.ABhaventWin = True
        self.indicator = 0
        self.extractscore = 0
        self.message = "Player 1's turn!"
        self.controller = controller
        self.parent = parent
        self.plankImage = Image.open("images/plank.png").resize((80, 30), Image.ANTIALIAS)
        self.loadPlankImage = ImageTk.PhotoImage(self.plankImage)
        self.playerMessage = Label(self.frame, text=self.message, compound=CENTER, font=1.5, bg="#4f3d21", fg="white")
        self.AIBtn = Label(self.frame, text='HINT', width="80", height="30", image=self.loadPlankImage, compound=CENTER, bg="#4f3d21", fg="white")
        self.AIMessage = Label(self.frame, text="Press on HINT!", bg="#4f3d21", fg="white")
        self.assignArray = []
        self.ABBSmove = -1


    def init_holes(self):
        for index in range(0, self.holes):
            indicator = False
            if index < self.holes / 2:
                indicator = True
            self.boardArray.append(Hole(self.beads, index, indicator))

        self.playerMessage.grid(row=2, columnspan=int(len(self.boardArray)), pady=15, padx=(20, 10))
        self.AIBtn.photo = self.loadPlankImage
        self.AIBtn.config(font=("Courier", 12, "bold"))
        self.AIBtn.grid(row=2, column=0)
        self.AIBtn.bind("<Button-1>", lambda event, a=self.boardArray: self.AlphaBetaTrigger(a))

    def left_click(self, iteration, cplayer):
        self.checkstatus(iteration, cplayer)

        if self.checkStatus == False:
            if cplayer != "CPU":
                messagebox.showerror("Error", "Please choose a hole with values or from your side!")
            return
        else:
            if cplayer == self.p1name:
                cplayer = self.p2name
                self.AIBtn.grid_forget()
                self.render_message("Player 2's Turn!")
                self.player1obj.assignScore(self.extractscore)
                self.checkHaventWin(cplayer)
                if self.haventWin == False:
                    self.player1obj.assignRemaining(self.boardArray)
                    self.controller.show_frame("GameOver", className=GameOver, player1Score=self.player1obj.currentScore, player2Score=self.player2obj.currentScore, player2Name=self.p2name)

                self.render_holes(cplayer)
                self.player1obj.render_player()
                self.player2obj.render_player()
                self.checkStatus = False

                if self.p2name == "CPU" and self.haventWin == True:
                    self.render_message("CPU's Turn!")
                    globalValues.screen.update()
                    time.sleep(1)

                    holeChosen = self.get_cpu_hole()
                    self.checkstatus(holeChosen, self.p2name)
                    cplayer = self.p1name
                    self.check_condition(cplayer)
                    self.render_message("Player 1's Turn!")
                    self.hintMsg = "Press on HINT for help!"
                    self.AIBtn.grid(row=2, column=0)
                    self.parent.render_ai_message(self.hintMsg)

            elif cplayer == self.p2name:
                self.AIBtn.grid(row=2, column=0)
                cplayer = self.p1name
                self.render_message("Player 1's Turn!")
                self.check_condition(cplayer)

            self.render_holes(cplayer)
            self.player1obj.render_player()
            self.player2obj.render_player()
            self.checkStatus = False

    def get_cpu_hole(self):
        while True:
            holeChosen = randint(len(self.boardArray) / 2, len(self.boardArray))
            if holeChosen < len(self.boardArray):
                if self.boardArray[holeChosen].beads != 0:
                    return holeChosen

    def check_condition(self, cplayer):
        self.player2obj.assignScore(self.extractscore)
        self.checkHaventWin(cplayer)

        if self.haventWin == False:
            self.player2obj.assignRemaining(self.boardArray)
            self.controller.show_frame("GameOver", className=GameOver, player1Score=self.player1obj.currentScore, player2Score=self.player2obj.currentScore, player2Name=self.p2name)

    def render_message(self, message):
        self.message = message
        self.playerMessage.configure(text=self.message)

    def create_hole(self, hole, hole_counter, row, currentPlayer):
        if hole.indicator == True and hole.beads != 0:
            image = Image.open("images/active-hole2.png").resize((100, 100), Image.ANTIALIAS)
        else:
            image = Image.open("images/hole2.png").resize((100, 100), Image.ANTIALIAS)
        if hole.iteration == self.ABBSmove:
            image = Image.open("images/hole-purple.png").resize((100, 100), Image.ANTIALIAS)
            self.ABBSmove = -1
            print("i'm in create_hole")

        loadImage = ImageTk.PhotoImage(image)
        label = Label(self.frame, image=loadImage, text=hole.beads, compound=CENTER, font=2.5, bg="#b2854b", fg="white")
        label.config(font=("Courier", 30))
        label.photo = loadImage
        label.grid(row=row, column=hole_counter)
        label.bind("<Button-1>", lambda event, iteration=hole.iteration, cplayer=currentPlayer: self.left_click(iteration, cplayer))
        return label

    def render_holes(self, currentPlayer):
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
                self.ABextractScore(board, ABnextIndex)
                if playerNum < 0:
                    self.ABcheck1stRow(board)
                elif playerNum > 0:
                    self.ABcheck2ndRow(board)
                if self.ABhaventWin == False:
                    self.ABassignRemaining(board)
        else:
            ABnextIndex -= len(board)

            if board[ABnextIndex].beads != 0:
                self.ABcalBeads(board, ABnextIndex, playerNum)
            else:
                self.ABextractScore(board, ABnextIndex)
                if playerNum < 0:
                    self.ABcheck1stRow(board)
                elif playerNum > 0:
                    self.ABcheck2ndRow(board)
                if self.ABhaventWin == False:
                    self.ABassignRemaining(board)

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

    def ABassignRemaining(self, board):
        for i in board:
            self.ABroundScore += i.beads
            self.assignArray.append(i.iteration)
            i.beads = 0
        print("Assigned score is a total of "+str(self.ABroundScore)+"by adding "+str(self.assignArray))
        self.assignArray = []

    def ABassignScore(self):
        return self.ABroundScore

    def ABextractScore(self, board, index):
        ABnewIndex = index + 1
        if ABnewIndex < len(board):
            self.ABroundScore = board[ABnewIndex].beads
            print("current round score is"+str(self.ABroundScore))
            board[ABnewIndex].beads = 0
        else:
            ABnewIndex -= len(board)
            self.ABroundScore = board[ABnewIndex].beads
            print("current round score is"+str(self.ABroundScore))
            board[ABnewIndex].beads = 0

    def GameStatus(self):
        if self.ABhaventWin:
            return True
        else:
            return False

    def ABcheck1stRow(self, board):
        for i in range(0, int(len(board) / 2)):
            if board[i].beads != 0:
                self.ABhaventWin = True
                print("ABhaventWin is "+str(self.ABhaventWin)+" aborted at index "+str(i))
                return
            else:
                self.ABhaventWin = False
                print("ABhaventWin is "+str(self.ABhaventWin))

    def ABcheck2ndRow(self, board):
        for i in range(int(len(board) / 2), len(board)):
            if board[i].beads != 0:
                self.ABhaventWin = True
                print("ABhaventWin is "+str(self.ABhaventWin)+" aborted at index "+str(i))
                return
            else:
                self.ABhaventWin = False
                print("ABhaventWin is "+str(self.ABhaventWin))

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
        alpha = -INFINITY
        beta = INFINITY
        boardCopy = copy.deepcopy(board)
        playerNum = 1
        branches = self.checkAvailableMoves_ExtractIndex(boardCopy, playerNum)
        bestScore = -INFINITY
        p1ABscore = 0
        p2ABscore = 0

        for i in branches:
            score = self.MinAB(boardCopy, i, playerNum, alpha, beta, p1ABscore, p2ABscore)
            alpha = max(alpha, score)
            if score > bestScore:
                self.ABBSmove = i
                bestScore = score
        self.ABcalBeads(boardCopy, self.ABBSmove, playerNum)
        p1ABscore = self.ABassignScore()
        self.hintMsg = str("Choose hole number "+str(self.ABBSmove+1)+" to secure "+str(p1ABscore)+" beads, winning your opponent by "+str(bestScore)+" beads if it plays out accordingly")
        self.parent.render_ai_message(self.hintMsg)
        self.render_holes(self.p1name)

    def MinAB(self, board, index, playerNum, alpha, beta, p1ABscore, p2ABscore):
        boardCopy = copy.deepcopy(board)
        self.ABcalBeads(boardCopy, index, playerNum)
        p1ABscore += self.ABassignScore()
        ABhaventWin = self.GameStatus()
        playerNum = -1
        branches = self.checkAvailableMoves_ExtractIndex(boardCopy, playerNum)
        score = INFINITY

        for i in branches:
            score = min(score, self.MaxAB(boardCopy, i, playerNum, alpha, beta, p1ABscore, p2ABscore))

            beta = min(beta, score)
            if alpha >= beta:
                return score
            return score

        if len(branches) == 0:
            if ABhaventWin == False:
                score = p1ABscore - p2ABscore
        return score

    def MaxAB(self, board, index, playerNum, alpha, beta, p1ABscore, p2ABscore):
        boardCopy = copy.deepcopy(board)
        self.ABcalBeads(boardCopy, index, playerNum)
        p2ABscore += self.ABassignScore()
        ABhaventWin = self.GameStatus()
        playerNum = 1
        branches = self.checkAvailableMoves_ExtractIndex(boardCopy, playerNum)
        score = -INFINITY

        for i in branches:
            score = max(score, self.MinAB(boardCopy, i, playerNum, alpha, beta, p1ABscore, p2ABscore))

            alpha = max(alpha, score)
            if alpha >= beta:
                return score
            return score

        if len(branches) == 0:
            if ABhaventWin == False:
                score = p1ABscore - p2ABscore
        return score


