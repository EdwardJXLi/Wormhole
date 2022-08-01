from wormhole.video import AbstractVideo
from wormhole.controller import AbstractController

# General Abstract Streamer Class for Wormhole. 
class AbstractStreamer():
    def __init__(self, controller: AbstractController, video: AbstractVideo, route: str, frame_rate: int = 30):
        self.controller = controller
        self.video = video
        self.route = route
        self.frame_rate = frame_rate
