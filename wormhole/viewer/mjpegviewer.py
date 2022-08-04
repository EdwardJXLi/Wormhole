from wormhole.viewer import AbstractViewer
from wormhole.utils import FrameController

from threading import Thread
import cv2
import urllib.request
import numpy as np
import traceback

# Viewer for the Motion JPEG video protocol    
class MJPEGViewer(AbstractViewer):
    def __init__(
        self, 
        url: str, 
        height: int, 
        width: int, 
        max_fps: int = 30, 
        auto_reconnect: bool = True
    ):
        # Save basic variables about stream
        self.url = url
        self.auto_reconnect = auto_reconnect
        
        # Open Video Link
        self.cap = cv2.VideoCapture(self.url)
        # Set height and width
        # height = height or int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # width = width or int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        
        super().__init__(height, width, max_fps=max_fps)
        
        # Check if Video File Opened
        if not self.cap.isOpened():
            raise ValueError("Video File Not Opened! An Error Probably Occurred.")
        # Set up Frame Controller
        self.frame_controller = FrameController(self.max_fps)
        
        # Start Video Thread
        self.video_decoder_thread = Thread(target=self.video_decoder, daemon = True)
        self.video_decoder_thread.start()
        
    def video_decoder(self):
        # Start Video Loop
        while True:
            # Read Frame
            ret, frame = self.cap.read()
            # Check if Frame is Valid
            if not ret:
                if self.auto_reconnect:
                    retry_fc = FrameController(1)
                    while True:
                        self.cap = cv2.VideoCapture(self.url)
                        if not self.cap.isOpened():
                            print("Failed to connect to stream... Retrying in 1 second...")
                            retry_fc.next_frame()
                        else:
                            print("Stream Reconnected!")
                            # Reset fps stats for video controller
                            self.frame_controller.reset_fps_stats()
                            break
                    continue
                else:
                    self.set_blank_frame()                 
            # Set Frame
            self.set_frame(frame)
            self.frame_controller.next_frame()
    
# Alternative implementation of the MJPEGViewer class
class MJPEGViewerRaw(AbstractViewer):
    def __init__(
        self, 
        url: str, 
        height: int, 
        width: int, 
        max_fps: int = 30, 
        read_buffer_size: int = 1024, 
        auto_reconnect: bool = True
    ):
        # Save basic variables about stream
        self.url = url
        self.auto_reconnect = auto_reconnect
        
        # Save advanced variables about stream
        self.read_buffer_size = read_buffer_size
        
        # Start the video decoder in another thread
        self.video_decoder_thread = Thread(target=self.video_decoder, daemon=True)
        self.video_decoder_thread.start()
        
        # Create Object
        super().__init__(height, width, max_fps=max_fps)
       
    # Video Decoder Thread 
    def video_decoder(self):
        while True:
            try:
                with urllib.request.urlopen(self.url) as stream:
                    # Read jpeg image from stream
                    inBytes = bytes()
                    # TODO: Find a way to make this faster
                    while True:
                        inBytes += stream.read(self.read_buffer_size)
                        a = inBytes.find(b'\xff\xd8')
                        b = inBytes.find(b'\xff\xd9')
                        if a != -1 and b != -1:
                            jpg = inBytes[a:b+2]
                            inBytes = inBytes[b+2:]
                            np_image = np.fromstring(jpg, dtype=np.uint8)  # type: ignore
                            i = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
                            self.set_frame(i)
            except Exception as e:
                if self.auto_reconnect:
                    print(f"Open Camera Error: {e}")
                    traceback.print_exc()
                else:
                    self.set_blank_frame()
