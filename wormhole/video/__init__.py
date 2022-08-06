import cv2
import numpy as np
import traceback
from typing import Callable, Optional
from wormhole.utils import FrameController


class AbstractVideo():
    """
    General Abstract Video Class for Wormhole. Has some advanced features that are helpful for video processing
    """

    def __init__(
        self,
        height: int,
        width: int,
        max_fps: float = 30,
        print_fps: bool = False
    ):
        # Basic Video Properties
        self.height: int = height
        self.width: int = width
        self.max_fps: float = max_fps
        self.print_fps = print_fps
        
        # Sanity Check
        if 0 > self.height or 0 > self.width or 0 > self.max_fps:
            raise ValueError("Video Properties cannot smaller than 0!")
        
        # Video Information
        self._frame: np.ndarray = np.zeros((height, width, 3), np.uint8)
        self.finished_frame: np.ndarray = self._frame
        
        # Frame Modifiers -> List of functions that change the output video when a new frame arrives
        self.frame_modifiers: list[Callable[[AbstractVideo], None]] = []
        # Frame Subscribers -> List of functions to call when a new frame arrives
        self.frame_subscribers: list[Callable[[AbstractVideo], None]] = []
        # Set up Frame Controller
        self.frame_controller = FrameController(self.max_fps, print_fps=self.print_fps)

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


def render_video(
    video: AbstractVideo,
    height: Optional[int] = None,
    width: Optional[int] = None,
    max_fps: Optional[float] = None,
    print_fps: bool = False,
    window_name="Video Preview"
):
    height = height or video.height
    width = width or video.width
    max_fps = max_fps or video.max_fps
    frame_controller = FrameController(max_fps, print_fps=print_fps)
    while True:
        frame = video.get_frame()
        cv2.imshow(window_name, cv2.resize(frame, (width, height)))
        if cv2.waitKey(1) == ord('q'):
            break
        frame_controller.next_frame()
    cv2.destroyAllWindows()

# Create an alias for AbstractVideo for a more coherent API


class CustomVideo(AbstractVideo):
    """
    Create Custom Video Streams
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
