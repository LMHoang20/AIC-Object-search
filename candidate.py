from frame import Frame 

class Candidate:
    def __init__(self, frame: Frame, score: float):
        self.frame = frame
        self.score = score
