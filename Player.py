class Player:

    def __init__(self, name):
        self.name = name
        self.currentScore = 0

    def assignScore(self, index, daboard):
        self.newIndex = index + 1
        if self.newIndex < len(daboard):
            self.currentScore += daboard[self.newIndex]
            daboard[self.newIndex] = 0
        else:
            self.newIndex -= len(daboard)
            self.currentScore += daboard[self.newIndex]
            daboard[self.newIndex] = 0

    def getCurrentScore(self):
        return int(self.currentScore)