from wormhole.video import AbstractVideo
from wormhole.controller import AbstractController

# General Abstract Streamer Class for Wormhole. 
class AbstractStreamer():
    def __init__(
        self, 
        controller: AbstractController, 
        video: AbstractVideo, 
        route: str, 
        strict_url: bool = True
    ):
        self.controller = controller
        self.video = video
        self.route = route
        self.strict_url = strict_url
