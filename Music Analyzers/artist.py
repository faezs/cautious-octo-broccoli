import numpy
import Models

class Artist:

    def __init__(self):
        self.score = []
        self.works = []
        self.model = "Concatenated Works"

    def __getattr__(self, attribute):
            return self.attribute
