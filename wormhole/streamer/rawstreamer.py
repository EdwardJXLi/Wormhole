from wormhole.streamer import AbstractStreamer
from wormhole.utils import FrameController

from flask_socketio import emit, join_room
from threading import Thread
from typing import Optional, Any
import cv2

# Base Class for All Raw Image Streaming Formats
class RawStreamerBase(AbstractStreamer):
    def __init__(
        self, 
        encode_format: str,
        *args, 
        boundary: str = "WORMHOLE", 
        fps_override: Optional[int] = None, 
        imencode_config: Optional[list[Any]] = None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        
        # Setup Basic Vars
        self.encode_format = encode_format
        self.boundary = boundary
        self.max_fps = fps_override or self.video.max_fps
        self.imencode_config = imencode_config
        
        # Control variables to save on execution when no clients are connected
        self.thread_running = False
        self.connected_clients = 0
        
        # Create Background Video Streamer
        def video_streamer_loop():
            # Get the flask context
            with self.controller.get_app().app_context():
                frame_controller = FrameController(self.max_fps)
                while True:
                    if not self.thread_running:
                        return  # Kill the thread if no clients are connected
                    
                    _, jpg = cv2.imencode(
                        self.encode_format, 
                        self.video.get_frame(),
                        self.imencode_config or []  # Use Empty Config if imencode is not available
                    )
                    emit("video_frame", jpg.tobytes(), room="video_feed", namespace=self.route, broadcast=True)
                    frame_controller.next_frame()

        # Setup Background Video Thread
        self.video_streamer_thread = Thread(target=video_streamer_loop)
                
        # Add Connect Handler
        def on_connect():
            self.connected_clients += 1
            # Start the video streamer if it is not already running
            if self.thread_running == False:
                self.thread_running = True
                self.video_streamer_thread = Thread(target=video_streamer_loop)
                self.video_streamer_thread.start()
            
            # Tell client to join the video room
            join_room("video_feed")
        self.controller.add_message_handler("connect", on_connect, namespace=self.route, strict_url=self.strict_url)
        
        # Add Disconnect Handler
        def on_disconnect():
            self.connected_clients -= 1
            
            # If no clients are connected anymore, stop server
            if self.connected_clients == 0:
                self.thread_running = False
        self.controller.add_message_handler("disconnect", on_disconnect, namespace=self.route, strict_url=self.strict_url)

# Below are the different image encoding types the system supports

# Raw JPEG Streamer
class RawJPEGStreamer(RawStreamerBase):
    def __init__(self, *args, **kwargs):
        super().__init__(".jpg", *args, **kwargs)
