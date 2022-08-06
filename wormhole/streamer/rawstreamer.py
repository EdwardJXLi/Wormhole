from wormhole.streamer.socketiostreamer import SocketIOStreamerBase

from typing import Optional, Any
import cv2

# Raw Image Streaming
# This is generally not recommended as it sends A LOT of information over the network, 
# But its an interesting experiment to see the maximum processing throughput
# Without any image encoding
class RawStreamer(SocketIOStreamerBase):
    def __init__(
        self, 
        *args,
        **kwargs
    ):
        # Initiate Parent SocketIO Streamer Object
        super().__init__(self.stream_hotloop, *args, **kwargs)
    
    # Hotloop for sending raw video
    def stream_hotloop(self):
        self.send_data(self.video.get_frame().tobytes())
        

# Raw JPEG Streaming
# Sends raw individual JPEG frames over the network
class RawJPEGStreamer(SocketIOStreamerBase):
    def __init__(
        self, 
        *args,
        imencode_config: Optional[list[Any]] = None,
        **kwargs
    ):
        # Initiate Parent SocketIO Streamer Object
        super().__init__(self.stream_hotloop, *args, **kwargs)
        
        # Setup some configs for the imencode function
        self.imencode_config = imencode_config
    
    # Hotloop for sending raw video
    def stream_hotloop(self):
        _, jpg = cv2.imencode(
            ".jpg", 
            self.video.get_frame(),
            self.imencode_config or []  # Use Empty Config if imencode is not available
        )
        self.send_data(jpg.tobytes())
