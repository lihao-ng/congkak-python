class Board:

    def __init__(self, holes, beads, p1name, p2name):
        self.holes = holes
        self.beads = beads
        self.boardArray = []
        self.p1name = p1name
        self.p2name = p2name
        self.p1side = 0
        self.p2side = 0
        self.checkStatus = True
        self.haventWin = True

        for x in range(self.holes):
            self.boardArray.append(beads)

    def bord(self):
        i=0
        for x in self.boardArray:
            print(str(x)+"-"+str(i))
            i += 1

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
            if self.boardArray[self.nextIndex] != 0:
                print("\nCurrently at evalBeads after calBeads, going to call calBeads next!")
                self.calBeads(self.nextIndex)
            else:
                self.exportIndexfor = self.nextIndex
        else:
            self.nextIndex -= len(self.boardArray)

            if self.boardArray[self.nextIndex] != 0:
                self.calBeads(self.nextIndex)
            else:
                self.exportIndexfor = self.nextIndex

    def calBeads(self, index):
        self.move = self.boardArray[index]
        self.boardArray[index] = 0
        print("self.move is"+str(self.move))

        self.z = 1
        for i in range(self.move):
            print("z b4 addition is "+str(self.z))
            self.newIndex = index + self.z
            print("self.newIndex is "+str(self.newIndex))
            if self.newIndex < len(self.boardArray):
                self.boardArray[self.newIndex] += 1
                print("\ncurrently at < arraylength self.newIndex "+str(self.newIndex)+" with a value of "+str(self.boardArray[self.newIndex]))
                print(self.boardArray)
                print("addition done\n")
            else:
                self.newIndex -= len(self.boardArray)
                print(str(self.newIndex)+" is newIndex"+str(len(self.boardArray))+" is array length")
                self.boardArray[self.newIndex] += 1
                print("\ncurrently at > arraylength self.newIndex " + str(self.newIndex) + " with a value of " +
                      str(self.boardArray[self.newIndex]))
                print(self.boardArray)
                print("addition done\n")
            self.z += 1
        print(str(self.newIndex)+" is self.newIndex")
        index = self.newIndex
        print(str(index)+" is index")
        print("moves have finished\n")
        self.evalBeads(index)

    def checkstatus(self, index, pname):
        if pname == self.p1name:
            if self.p1side == "1st":
                if index >= 0 and index < int(len(self.boardArray) / 2):
                    print("checking p1 1st row")
                    self.check1stRow()
                    if self.boardClear == False:
                        print("boardClear pass calling checkAmt now\n")
                        self.checkAmt(index)
                    else:
                        return
                else:
                    return
            else:
                if index >= int(len(self.boardArray) / 2) and index < len(self.boardArray):
                    print("checking p1 2nd row")
                    self.check2ndRow()
                    if self.boardClear == False:
                        print("boardClear pass calling checkAmt now\n")
                        self.checkAmt(index)
                    else:
                        return
                else:
                    return
        else:
            if self.p2side == "1st":
                if index >= 0 and index < int(len(self.boardArray) / 2):
                    print("checking p2 1st row\n")
                    self.check1stRow()
                    if self.boardClear == False:
                        print("boardClear pass calling checkAmt now\n")
                        self.checkAmt(index)
                    else:
                        return
                else:
                    return
            else:
                if index >= int(len(self.boardArray) / 2) and index < len(self.boardArray):
                    print("checking p2 2nd row")
                    self.check2ndRow()
                    if self.boardClear == False:
                        print("boardClear pass calling checkAmt now\n")
                        self.checkAmt(index)
                    else:
                        return
                else:
                    return

    def checkHaventWin(self, pname):
        if pname == self.p1name:
            if self.p1side == "1st":
                    self.check1stRow()
                    if self.boardClear == False:
                        print("board not empty yet")
                    else:
                        return
            else:
                    self.check2ndRow()
                    if self.boardClear == False:
                        print("board not empty yet")
                    else:
                        return
        else:
            if self.p2side == "1st":
                    self.check1stRow()
                    if self.boardClear == False:
                        print("board not empty yet")
                    else:
                        return
            else:
                    self.check2ndRow()
                    if self.boardClear == False:
                        print("board not empty yet")
                    else:
                        return

    def check1stRow(self):
        print("in check1strow\n")
        for i in range(0, int(len(self.boardArray) / 2)):
            if self.boardArray[i] != 0:
                self.boardClear = False
                self.haventWin = True
                print("board is not clear, array index "+str(i)+" is not empty with value "+str(self.boardArray[i]))
                return
            else:
                self.boardClear = True
                self.haventWin = False
                print("board is clear, array index "+str(i)+" is empty with value "+str(self.boardArray[i]))

    def check2ndRow(self):
        print("in check2ndrow \n")
        for i in range(int(len(self.boardArray) / 2), len(self.boardArray)):
            if self.boardArray[i] != 0:
                self.boardClear = False
                self.haventWin = True
                print("board is not clear, array index "+str(i)+" is not empty")
                return
            else:
                self.boardClear = True
                self.haventWin = False
                print("board is clear, array index "+str(i)+" is empty with value "+str(self.boardArray[i]))

    def checkAmt(self, index):
        if self.boardArray[index] != 0:
            self.checkStatus = False
            self.calBeads(index)
        else:
            print("hole is empty cannot choose this hole")
            return

    def exportIndex(self):
        return self.exportIndexfor

