from wormhole.utils import FrameController
from wormhole.viewer import AbstractViewer

import cv2
import math
import numpy as np
import traceback
import urllib.request
from threading import Thread


class MJPEGViewer(AbstractViewer):
    """
    Viewer for the Motion JPEG video protocol
    """

    def __init__(
        self,
        url: str,
        width: int,
        height: int,
        max_fps: float = 30,
        auto_reconnect: bool = True,
        **kwargs  # Any Additional Arguments for AbstractVideo
    ):
        # Save basic variables about stream
        self.url = url
        self.auto_reconnect = auto_reconnect

        # Open Video Link
        self.cap = cv2.VideoCapture(self.url)

        # Initiate Video Parent
        super().__init__(width, height, max_fps, **kwargs)

        # Check if Video File Opened
        if not self.cap.isOpened():
            raise ValueError("Video File Not Opened! An Error Probably Occurred.")

        # Start Video Thread
        self.video_decoder_thread = Thread(target=self.video_decoder, daemon=True)
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

            # If sizes does not match, resize frame
            frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            if frame_width != self.width or frame_height != self.height:
                frame = cv2.resize(frame, (self.width, self.height))

            # Set Frame
            self.set_frame(frame)
            self.frame_controller.next_frame()


class BufferedMJPEGViewer(AbstractViewer):
    """
    Alternative implementation of the MJPEGViewer class
    """

    def __init__(
        self,
        url: str,
        width: int,
        height: int,
        max_fps: float = math.inf,
        read_buffer_size: int = 1024,
        auto_reconnect: bool = True,
        **kwargs  # Any Additional Arguments for AbstractVideo
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
        super().__init__(width, height, max_fps, **kwargs)

    # Video Decoder Thread
    def video_decoder(self):
        while True:
            try:
                with urllib.request.urlopen(self.url) as stream:
                    # Read jpeg image from stream
                    inBytes = bytes()

                    # TODO: Find a way to make this faster
                    while True:
                        # Find start and end of image file
                        inBytes += stream.read(self.read_buffer_size)
                        a = inBytes.find(b'\xff\xd8')
                        b = inBytes.find(b'\xff\xd9')
                        if a != -1 and b != -1:
                            # Extract image from stream
                            jpg = inBytes[a:b + 2]
                            inBytes = inBytes[b + 2:]

                            # Decode Image
                            np_image = np.fromstring(jpg, dtype=np.uint8)  # type: ignore
                            new_frame = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

                            # If sizes does not match, resize frame
                            frame_height, frame_width, _ = new_frame.shape
                            if frame_width != self.width or frame_height != self.height:
                                new_frame = cv2.resize(new_frame, (self.width, self.height))

                            # Set the frame information
                            self.set_frame(new_frame)
                            self.frame_controller.next_frame()

            # Catch any errors that may occur in the video decoder
            except Exception as e:
                if self.auto_reconnect:
                    print(f"Open Stream Error: {e}")
                    traceback.print_exc()
                else:
                    self.set_blank_frame()
