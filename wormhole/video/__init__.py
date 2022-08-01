import numpy as np
import cv2
from typing import Callable, Any
import traceback
from wormhole.utils import FrameController

# General Abstract Video Class for Wormhole. Has some advanced features that are helpful for video processing
class AbstractVideo():
    def __init__(self, height: int, width: int, max_fps: int = 30):
        # Basic Video Properties
        self.height: int = height
        self.width: int = width
        self.max_fps: int = max_fps
        # Sanity Check
        if 0 in (self.height, self.width, self.max_fps):
            raise ValueError("Video Properties cannot be 0!")
        # Video Information
        self._frame: np.ndarray = np.zeros((height, width, 3), np.uint8)
        self.finished_frame: np.ndarray = self._frame
        # Frame Modifiers -> List of functions that change the output video when a new frame arrives
        self.frame_modifiers: list[Callable[[AbstractVideo], None]] = []
        # Frame Subscribers -> List of functions to call when a new frame arrives
        self.frame_subscribers: list[Callable[[AbstractVideo], None]] = []
        
    # Add a function to the frame modifiers
    def add_frame_modifier(self, modifier):
        self.frame_modifiers.append(modifier)
        
    # Add a function to the frame subscribers
    def add_frame_subscriber(self, subscriber):
        self.frame_subscribers.append(subscriber)
        
    # Call all frame modifiers
    def call_frame_modifiers(self):
        for modifier in self.frame_modifiers:
            try:
                modifier(self)
            except Exception as e:
                traceback.print_exc()
            
    # Call all frame subscribers
    def call_frame_subscribers(self):
        for subscriber in self.frame_subscribers:
            try:
                subscriber(self)
            except Exception as e:
                traceback.print_exc()
            
    # Get the current frame
    def get_frame(self):
        return self.finished_frame
        
    # Set the current frame
    def set_frame(self, frame: np.ndarray):
        self._frame = frame
        self.call_frame_modifiers()
        self.finished_frame = self._frame
        self.call_frame_subscribers()
        
    # Set the current frame to a blank frame
    def set_blank_frame(self):
        new_frame = np.zeros((self.height, self.width, 3), np.uint8)
        self.set_frame(new_frame)
        
    # Set the current frame to a blank frame with a given color
    def set_blank_frame_color(self, color: tuple):
        new_frame = np.zeros((self.height, self.width, 3), np.uint8)
        new_frame[:,:,:] = color
        self.set_frame(new_frame)
        
    # Set the current frame to a blank frame with a given color
    def set_blank_frame_color_rgb(self, r: int, g: int, b: int):
        new_frame = np.zeros((self.height, self.width, 3), np.uint8)
        new_frame[:,:,:] = (r, g, b)
        self.set_frame(new_frame)
        
def render_video(video: AbstractVideo, height: int = 720, width: int = 1280, fps: int = 30):
    fc = FrameController(fps)
    while True:
        frame = video.get_frame()
        cv2.imshow('frame', cv2.resize(frame, (width, height)))
        if cv2.waitKey(1) == ord('q'):
            break
        fc.next_frame()
    cv2.destroyAllWindows()
