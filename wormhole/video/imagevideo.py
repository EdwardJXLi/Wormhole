from wormhole.utils import FrameController
from wormhole.video import AbstractVideo

import cv2
import math
from threading import Thread
from typing import Any, Optional


class ImageVideo(AbstractVideo):
    """
    Creates a video object from an image file.
    NOTE: Setting max_fps will cause the video to re-read the image every frame!
    """

    def __init__(
        self, 
        filename: str,
        max_fps: Optional[float] = math.inf,
        width: Optional[int] = None,
        height: Optional[int] = None,
        **kwargs  # Any Additional Arguments for AbstractVideo
    ):
        # Basic Video Properties
        self.filename: str = filename

        # Open Image File
        self.image = cv2.imread(self.filename)
        
        # Check if the image opens properly
        if self.image is None:
            raise ValueError("Image File Not Opened! An Error Probably Occurred.")
        
        # Get info from image
        image_height, image_width = self.image.shape[:2]
        
        # Set width, height or fps if they are not set by default
        width = width or int(image_width)
        height = height or int(image_height)
        max_fps = max_fps or math.inf

        # Initialize Video Object
        super().__init__(width, height, max_fps, **kwargs)
        
        # Render the first instance of the image
        self.render()

        # Set up Frame Controller
        self.frame_controller = FrameController(self.max_fps, print_fps=self.print_fps)

        # If the user defined an FPS to use, start the image rendering thread
        if self.max_fps != math.inf:
            # Start Video Thread
            self.image_rendering_thread = Thread(target=self.video_loop, daemon=True)
            self.image_rendering_thread.start()
        
    def render(self, reopen_file: bool = False):
        # If user requests to reopen image file, do so
        if reopen_file:
            # Open Image File
            self.image = cv2.imread(self.filename)
            
            # Check if the image opens properly
            if self.image is None:
                raise ValueError("Image File Not Opened! An Error Probably Occurred.")
            
        # Get the new image
        new_frame = self.image.copy()
        
        # If sizes does not match, resize image
        frame_height, frame_width, _ = self.image.shape
        if frame_width != self.width or frame_height != self.height:
            new_frame = cv2.resize(new_frame, (self.width, self.height))
            
        # Set this image as the new frame
        self.set_frame(new_frame)
            
    def video_loop(self):
        # Start Video Loop
        while True:
            # Run render function to generate next frame
            self.render()
            self.frame_controller.next_frame()
