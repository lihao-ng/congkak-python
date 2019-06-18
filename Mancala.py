# from Board import *
# from Player import *
# from random import *
# from tkinter import *
#
# eholes = True
# w2 = True
# holes = 1
# players = True
#
#
# p1name = input("Please enter the name of player 1: \n")
# player1 = Player(p1name)
#
# while players:
#     cpu = input("Would like you your 2nd player to be a CPU? ( y or n )")
#
#     if cpu == "y":
#         player2 = Player("CPU")
#         players = False
#     elif cpu == "n":
#         p2name = input("Please enter the name of player 2: \n")
#         player2 = Player(p2name)
#         players = False
#     else:
#         print("Please enter y or n")
#
#
# holes = int(input("Please enter the number of holes of your board: \n"))
# while holes % 2 !=0:
#     if holes % 2 != 0:
#         print("Please enter an even number for your number of holes!")
#         holes = int(input("Please enter the number of holes of your board: \n"))
#     elif holes % 2 == 0:
#         eholes = False
#         print("")
#
# beads = int(input("Please enter the number of beads in one hole: \n"))
#
#
# my_board = Board(holes, beads, player1.name, player2.name)
#
# print(my_board.boardArray)
# currentPlayer = player1.name
# print(player1.name)
# while w2:
#     side = input("Player 1 would you like to take the first half of the board? ( y / n )\n")
#
#     if side == "y":
#         my_board.chooseSide(side)
#         w2 = False
#     elif side == "n":
#         my_board.chooseSide(side)
#         w2 = False
#     else:
#         print("Please enter a valid answer Player 1! Type 'y' for yes & 'n' for no!")
#
#
# while my_board.haventWin:
#     my_board.checkStatus = True
#     while my_board.checkStatus:
#         if currentPlayer == "CPU":
#             holeChosen = randint(0, len(my_board.boardArray))
#             my_board.checkstatus(holeChosen, currentPlayer)
#         else:
#             holeChosen = int(input(currentPlayer+" please enter the hole that you want to choose\n :"))
#
#             if holeChosen < len(my_board.boardArray):
#                 my_board.checkstatus(holeChosen, currentPlayer)
#             else:
#                 print("\nPlease enter a valid hole as the previous one that you entered have exceeded the total number of holes")
#             if my_board.checkStatus:
#                 print("Please choose a hole that is present in your row")
#                 print("It is "+str(currentPlayer)+"'s turn now")
#
#     roundScore = my_board.exportScore()
#
#     print("roundScore is " + str(roundScore))
#
#     if currentPlayer == player1.name:
#         player1.assignScore(roundScore)
#         print(player1.name+"'s turn has ended!\n His score is "+str(player1.getCurrentScore()))
#         currentPlayer = player2.name
#         print("It is "+str(player2.name)+"'s turn next")
#     elif currentPlayer == player2.name:
#         player2.assignScore(roundScore)
#         print(player2.name+"'s turn has ended!\n His score is "+str(player2.getCurrentScore()))
#         currentPlayer = player1.name
#         print("It is "+str(player1.name)+"'s turn next")
#
#     my_board.checkHaventWin(currentPlayer)
#     print(my_board.boardArray)
#     """if currentPlayer == 1:
#         player1.assignScore(roundScore, my_board.boardArray)
#     elif currentPlayer == 2:
#         player1.getCurrentScore()
#     else:
#         print("")"""
# if currentPlayer == player1.name:
#     for i in my_board.boardArray:
#         player2.currentScore += i
# else:
#     for i in my_board.boardArray:
#         player1.currentScore += i
#
# if player1.getCurrentScore() > player2.getCurrentScore():
#     print("Player "+str(player1.name)+" wins!")
#     print(str(player1.name)+"'s score is "+str(player1.getCurrentScore()))
#     print(str(player2.name)+"'s score is "+str(player2.getCurrentScore()))
# elif player1.getCurrentScore() == player2.getCurrentScore():
#     print("It is a draw between Player "+str(player1.name)+" & Player "+str(player2.name))
#     print(str(player1.name)+"'s score is "+str(player1.getCurrentScore()))
#     print(str(player2.name)+"'s score is "+str(player2.getCurrentScore()))
# else:
#     print("Player "+str(player2.name)+" wins!")
#     print(str(player1.name)+"'s score is "+str(player1.getCurrentScore()))
#     print(str(player2.name)+"'s score is "+str(player2.getCurrentScore()))
