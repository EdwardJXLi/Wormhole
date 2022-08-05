from wormhole.streamer.socketiostreamer import SocketIOStreamerBase
from wormhole.utils import FrameController

from flask_socketio import emit
import time
from typing import Optional

# Raw Image Streaming
# This is generally not recommended as it sends A LOT of information over the network, 
# But its an interesting experiment to see the maximum processing throughput
# Without any image encoding
class RawStreamer(SocketIOStreamerBase):
    def __init__(
        self, 
        *args,
        fps_override: Optional[int] = None, 
        **kwargs
    ):
        # Initiate Parent SocketIO Streamer Object
        super().__init__(self.video_streamer, *args, **kwargs)
        
        # Setup Basic Vars
        self.max_fps = fps_override or self.video.max_fps
    
    # Streamer hotloop for raw video
    def video_streamer(self):
        # Get the flask context
        with self.controller.get_app().app_context():
            frame_controller = FrameController(self.max_fps)
            while True:
                if not self.thread_running:
                    return  # Kill the thread if no clients are connected
                
                emit("frame", self.video.get_frame().tobytes(), room="video_feed", namespace=self.route, broadcast=True)
                
                time.sleep(0)  # Force A Network Buffer Flush
                # Technically this should be a gevent.sleep(0) but time.sleep is monkey patched so this should be alright.
                
                frame_controller.next_frame()
