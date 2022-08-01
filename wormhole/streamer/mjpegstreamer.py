from wormhole.streamer import AbstractStreamer
from wormhole.utils import FrameController

from flask.wrappers import Response
import cv2

# Streamer for the Motion JPEG video protocol
class MJPEGStreamer(AbstractStreamer):
    def __init__(self, *args, boundary: str = "WORMHOLE", **kwargs):
        super().__init__(*args, **kwargs)

        # Create Video Feed Handler for Flask
        def video_feed():
            # Render and Send Frames for each client
            def generate_next_frame():
                frame_controller = FrameController(self.frame_rate)
                while True:
                    _, jpg = cv2.imencode(
                        ".jpg", self.video.get_frame()
                    )
                    yield (b"--" + boundary.encode("ascii") + b"\r\nContent-Type: image/jpeg\r\n\r\n" + jpg.tobytes() + b"\r\n")
                    frame_controller.next_frame()

            return Response(
                generate_next_frame(),
                mimetype=f"multipart/x-mixed-replace; boundary={boundary}",
            )
        
        # Add the video feed route to the network controller
        self.controller.add_route(self.route, video_feed)
