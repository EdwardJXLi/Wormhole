from wormhole.utils import FrameController
from wormhole.video import AbstractVideo

import numpy as np
from threading import Thread
from typing import Callable, Optional


class CustomVideo(AbstractVideo):
    """
    Creates a video object from a custom video stream.
    Takes in a video_generator function that returns a new frame every time it is called.
    """

    def __init__(
        self,
        width: int,
        height: int,
        max_fps: float,
        frame_generator: Optional[Callable] = None,
        **kwargs  # Any Additional Arguments for AbstractVideo
    ):
        # Basic Video Properties
        self.frame_generator: Optional[Callable] = frame_generator

        # Initialize Video Object
        super().__init__(width, height, max_fps, **kwargs)

        # Set up Frame Controller
        self.frame_controller = FrameController(self.max_fps, print_fps=self.print_fps)

        # Start Video Thread
        # If frame generator is defined, start the video thread.
        # ELSE, the user probably wants to set frames manually by calling set_frame(), so dont start thread
        if self.frame_generator:
            self.video_generator_thread = Thread(target=self.video_loop, daemon=True)
            self.video_generator_thread.start()
        else:
            pass

    def video_loop(self):
        # Start Video Loop
        while True:
            try:
                if self.frame_generator:
                    # Get a new frame from the frame generator
                    frame = self.frame_generator(self)
                    # The frame generator might've already set the frame using set_frame(),
                    # so only run set_frame again if the return type is of ndarray
                    if isinstance(frame, np.ndarray):
                        self.set_frame(frame)
                    self.frame_controller.next_frame()
                else:
                    raise Exception("Frame generator not defined during video loop! This should not happen normally")
            except Exception as e:
                self.handle_render_error(e, message="Frame Generator Encountered An Error!")
