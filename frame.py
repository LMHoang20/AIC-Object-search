class Frame:
    def __init__(self, video: str|None = None, frame_name: str|None = None, id: str|None = None) -> None:
        if id == None:
            self.video = video
            self.frame_name = frame_name
            self.id = video + '/' + frame_name
        else:
            self.id = id
            self.video, self.frame_name = self.id.split('/')
    
    def serialize(self) -> dict:
        return {
            'video': self.video,
            'frame_name': self.frame_name,
            'id': self.id,
        }
    