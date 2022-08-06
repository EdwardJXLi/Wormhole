from wormhole.controller import AbstractController
from wormhole.video import AbstractVideo

from typing import Optional

class AbstractStreamer():
    """
    General Abstract Streamer Class for Wormhole.
    """

    def __init__(
        self,
        controller: AbstractController,
        video: AbstractVideo,
        route: str,
        fps_override: Optional[float] = None,
        print_fps: bool = False,
        strict_url: bool = True
    ):
        self.controller = controller
        self.video = video
        self.route = route
        self.max_fps = fps_override or self.video.max_fps
        self.print_fps = print_fps
        self.strict_url = strict_url
