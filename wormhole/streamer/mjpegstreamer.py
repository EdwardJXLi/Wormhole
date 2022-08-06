from wormhole.streamer import AbstractStreamer
from wormhole.utils import FrameController

import cv2
from flask.wrappers import Response
from typing import Optional, Any


class MJPEGStreamer(AbstractStreamer):
    """
    Streamer for the Motion JPEG video protocol
    """

    def __init__(
        self,
        *args,
        boundary: str = "WORMHOLE",
        imencode_config: Optional[list[Any]] = None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.boundary = boundary
        self.imencode_config = imencode_config

        # Create Video Feed Handler for Flask
        def video_feed():
            # Render and Send Frames for each client
            def generate_next_frame():
                frame_controller = FrameController(self.max_fps, print_fps=self.print_fps)
                while True:
                    _, jpg = cv2.imencode(
                        ".jpg",
                        self.video.get_frame(),
                        self.imencode_config or []  # Use Empty Config if imencode is not available
                    )
                    yield (b"--" + boundary.encode("ascii") + b"\r\nContent-Type: image/jpeg\r\n\r\n" + jpg.tobytes() + b"\r\n")
                    frame_controller.next_frame()

            return Response(
                generate_next_frame(),
                mimetype=f"multipart/x-mixed-replace; boundary={boundary}",
            )

        # Add the video feed route to the network controller
        self.controller.add_route(self.route, video_feed, strict_url=self.strict_url)
