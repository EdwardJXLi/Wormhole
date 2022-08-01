from wormhole.video import AbstractVideo
from wormhole.controller import AbstractController

# General Abstract Streamer Class for Wormhole. 
class AbstractStreamer():
    def __init__(self, controller: AbstractController, video: AbstractVideo, route: str, ignore_url_check: bool = False):
        self.controller = controller
        self.video = video
        self.route = route
        self.ignore_url_check = ignore_url_check
