import logging
import numpy as np
import time
import traceback
from typing import Callable
from wormhole.utils import blank_frame_color, draw_text, FrameController


class AbstractVideo():
    """
    General Abstract Video Class for Wormhole. Has some advanced features that are helpful for video processing
    """

    def __init__(
        self,
        width: int,
        height: int,
        max_fps: float,
        pixel_size: int = 3,
        print_fps: bool = False,
        frame_modifiers=None,
        frame_subscribers=None
    ):
        # Basic Video Properties
        self.width: int = width
        self.pixel_size: int = pixel_size
        self.height: int = height
        self.max_fps: float = max_fps
        self.print_fps: bool = print_fps

        # Sanity Check
        if 0 > self.width or 0 > self.height or 0 > self.max_fps:
            raise ValueError("Video Properties cannot smaller than 0!")

        # Video Information
        self._frame: np.ndarray = np.zeros((width, height, self.pixel_size), np.uint8)
        self.finished_frame: np.ndarray = self._frame

        # Frame Modifiers -> List of functions that change the output video when a new frame arrives
        self.frame_modifiers: list[Callable[[AbstractVideo], None]] = frame_modifiers or []
        # Frame Subscribers -> List of functions to call when a new frame arrives
        self.frame_subscribers: list[Callable[[AbstractVideo], None]] = frame_subscribers or []
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
            except Exception as error:
                logging.error(f"Error While Running Frame Modifier {modifier}")
                traceback.print_exc()

                # Render error to video frame
                draw_text(self._frame, "ERROR!", (10, 60), font_color=(0, 0, 255), font_size=2, font_stroke=4)
                draw_text(self._frame, f"Error While Running Frame Modifier {modifier}!", (10, 100))
                draw_text(self._frame, f"Error: {error}", (10, 130), font_size=0.5, font_stroke=1)

    # Call all frame subscribers
    def call_frame_subscribers(self):
        for subscriber in self.frame_subscribers:
            try:
                subscriber(self)
            except Exception as e:
                logging.error(f"Error While Running Frame Subscriber {subscriber}")
                traceback.print_exc()

    # Get the current frame
    def get_frame(self):
        return self.finished_frame

    # Set the current frame
    def set_frame(self, frame: np.ndarray):
        # Sanity Check Frame Size
        if frame.size != self.width * self.height * self.pixel_size:
            raise ValueError(f"Frame Size Does Not Match! Frame Size: {frame.size}, Expected Size: {self.height * self.width * self.pixel_size}")

        # Set Frame
        self._frame = frame
        self.call_frame_modifiers()
        self.finished_frame = self._frame
        self.call_frame_subscribers()

    # Set the current frame to a blank frame
    def set_blank_frame(self):
        new_frame = np.zeros((self.width, self.height, self.pixel_size), np.uint8)
        self.set_frame(new_frame)

    def handle_render_error(self, error, message="Error While Generating Next Frame!"):
        try:
            # Print error to user
            logging.error(f"Error While Rendering Frame: {error}")
            traceback.print_exc()

            # Render an error video frame
            error_frame = blank_frame_color(self.width, self.height, (0, 0, 0))
            error_frame = draw_text(error_frame, "ERROR!", (10, 60), font_color=(0, 0, 255), font_size=2, font_stroke=4)
            error_frame = draw_text(error_frame, message, (10, 100))
            error_frame = draw_text(error_frame, f"Error: {error}", (10, 130), font_size=0.5, font_stroke=1)
            self.finished_frame = error_frame

            # Sleep one second so its not hotlooping like crazy
            time.sleep(1)

            # Reset FPS statistics in case the video works again
            self.frame_controller.reset_fps_stats()
        except Exception as e:
            print(f"Error while processing error frame!!!!! {e}")
            print(f"Something is seriously wrong with this video object or this instance of Wormhole!")
