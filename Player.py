class Player:

    def __init__(self, name):
        self.name = name
        self.currentScore = 0

    def assignScore(self, score):
        self.currentScore += score

    def getCurrentScore(self):
        return int(self.currentScore)