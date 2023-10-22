from frame import Frame 

class Candidate:
    def __init__(self, frame: Frame, score: float):
        self.frame = frame
        self.score = score

    def serialize(self) -> dict:
        return {
            'video': self.frame.video,
            'frame_name': self.frame.frame_name + '.jpg',
            'score': self.score,
        }