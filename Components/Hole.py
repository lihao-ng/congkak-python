class Hole:
    def __init__(self, beads, iteration, indicator):
        self.beads = beads
        self.iteration = iteration
        self.indicator = indicator

    def __repr__(self):
        return str(self.beads)