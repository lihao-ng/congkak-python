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
        self.ABroundScore = 0
        self.checkStatus = False
        self.haventWin = True
        self.ABhaventWin = True
        self.indicator = 0
        self.extractscore = 0
        self.message = "Player 1's turn!"
        self.controller = controller
        self.plankImage = Image.open("images/plank.png").resize((80, 30), Image.ANTIALIAS)
        self.loadPlankImage = ImageTk.PhotoImage(self.plankImage)
        self.playerMessage = Label(self.frame, text=self.message, compound=CENTER, font=1.5, bg="#4f3d21", fg="white")
        self.AIBtn = Label(self.frame, text='HINT', width="80", height="30", image=self.loadPlankImage, compound=CENTER, bg="#4f3d21", fg="white")
        self.assignArray = []

    def init_holes(self):
        for index in range(0, self.holes):
            indicator = False
            if index < self.holes / 2:
                indicator = True
            self.boardArray.append(Hole(self.beads, index, indicator))

        self.playerMessage.grid(row=2, columnspan=int(len(self.boardArray)), pady=15)
        self.AIBtn.photo = self.loadPlankImage
        self.AIBtn.config(font=("Courier", 12, "bold"))
        self.AIBtn.grid(row=2, column=0)
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
            image = Image.open("images/active-hole2.png").resize((100, 100), Image.ANTIALIAS)
        else:
            image = Image.open("images/hole2.png").resize((100, 100), Image.ANTIALIAS)

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
                self.ABextractScore(board, ABnextIndex)
                if playerNum < 0:
                    self.ABcheck1stRow(board)
                elif playerNum > 0:
                    self.ABcheck2ndRow(board)
                if self.ABhaventWin == False:
                    self.ABassignRemaining(board, playerNum)
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
        ABhaventWin = True
        self.ABcounter = 0
        print("branches at depth trigger "+str(self.ABcounter)+" is "+str(branches))

        for i in branches:
            print("branches at depth trigger "+str(self.ABcounter)+" is "+str(branches)+" with value of i="+str(i))
            score = self.MinAB(boardCopy, i, playerNum, alpha, beta, p1ABscore, p2ABscore, ABhaventWin)
            alpha = max(alpha, score)
            print(str(score)+" is the value of score at trigger & beta & alpha"+str(beta)+" & "+str(alpha))
            if score > bestScore:
                move = i
                bestScore = score
        self.ABcalBeads(boardCopy, move, playerNum)
        p1ABscore = self.ABassignScore()
        print("Index of move is "+str(move)+" and the best possible score is adding "+str(bestScore)+" to your current score, along with the next move score of "+str(p1ABscore))
        #return self.move, self.bestScore

    def MinAB(self, board, index, playerNum, alpha, beta, p1ABscore, p2ABscore, ABhaventWin):
        boardCopy = copy.deepcopy(board)
        self.ABcalBeads(boardCopy, index, playerNum)
        p1ABscore += self.ABassignScore()
        print("p1ABscore is "+str(p1ABscore))
        ABhaventWin = self.GameStatus()
        print("Game Status is "+str(ABhaventWin))
        playerNum = -1
        branches = self.checkAvailableMoves_ExtractIndex(boardCopy, playerNum)
        score = INFINITY
        print("branches at depth "+str(self.ABcounter)+" in MinAB is "+str(branches))

        for i in branches:
            score = min(score, self.MaxAB(boardCopy, i, playerNum, alpha, beta, p1ABscore, p2ABscore, ABhaventWin))
            print(str(score)+" is the value of score")
            print("The value of beta is "+str(beta)+"at depth "+str(self.ABcounter))

            beta = min(beta, score)
            print(str(beta)+" is the value of beta")
            #if score > alpha:
            if alpha >= beta:
                print("pruned at MinAB")
                return score
            return score

        if len(branches) == 0:
            if ABhaventWin == False:
                #p1ABscore += self.ABassignScore()
                print("p1ABscore is " + str(p1ABscore)+" after assigning remaining to him")
                score = p1ABscore
                print("game ends here\n")
            else:
                print("length of branches is " + str(len(branches)) + " and the game status is " + str(ABhaventWin))
                print("\n"+str(boardCopy)+"\n")
        self.ABcounter += 1
        return score

    def MaxAB(self, board, index, playerNum, alpha, beta, p1ABscore, p2ABscore, ABhaventWin):
        boardCopy = copy.deepcopy(board)
        self.ABcalBeads(boardCopy, index, playerNum)
        p2ABscore += self.ABassignScore()
        print("p2ABscore is "+str(p2ABscore))
        ABhaventWin = self.GameStatus()
        print("Game Status is "+str(ABhaventWin))
        playerNum = 1
        branches = self.checkAvailableMoves_ExtractIndex(boardCopy, playerNum)
        score = -INFINITY
        print("branches at depth "+str(self.ABcounter)+" in MaxAB is "+str(branches))
        for i in branches:
            score = max(score, self.MinAB(boardCopy, i, playerNum, alpha, beta, p1ABscore, p2ABscore, ABhaventWin))
            print(str(score)+" is the value of score")
            print("The value of alpha is "+str(alpha)+"at depth "+str(self.ABcounter))

            alpha = max(alpha, score)
            print(str(alpha)+" is the value of alpha")
            #if score < beta:
            if alpha >= beta:
                print("pruned at MaxAB")
                return score
            return score

        if len(branches) == 0:
            if ABhaventWin == False:
                #p2ABscore += self.ABassignScore()
                print("p2ABscore is " + str(p2ABscore)+" after assigning remaining to him")
                score = p2ABscore
                print("game ends here\n")
            else:
                print("length of branches is " + str(len(branches)) + " and the game status is " + str(ABhaventWin))
                print("\n"+str(boardCopy)+"\n")
        self.ABcounter += 1
        return score


