from wormhole.utils import FrameController
from wormhole.video import AbstractVideo

import cv2
from threading import Thread


class SoftCopy(AbstractVideo):
    """
    Creates a soft copy of another video stream. Uses Frame Subscribers to achieve this effect.
    """

    def __init__(
        self,
        original: AbstractVideo,
        print_fps: bool = False
    ):
        # Initialize Video Object with the original parameters
        super().__init__(original.height, original.width, original.max_fps, print_fps=print_fps)

        # Create a subscriber for the other video stream
        def video_update_subscriber(video):
            self.set_frame(video.get_frame())
            self.frame_controller.next_frame()
        original.add_frame_subscriber(video_update_subscriber)


class HardCopy(AbstractVideo):
    """
    Creates a hard copy of another video stream. Uses its own frame controller to achieve this effect
    """

    def __init__(
        self,
        original: AbstractVideo,
        height: int,
        width: int,
        max_fps: float = 30,
        print_fps: bool = False
    ):
        # Initialize Video Object with the NEW parameters
        super().__init__(height, width, max_fps=max_fps, print_fps=print_fps)
        self.original = original

        # Start Video Thread
        self.video_thread = Thread(target=self.video_loop, daemon=True)
        self.video_thread.start()

    def video_loop(self):
        # Start Video Loop
        while True:
            # Get the new video data
            new_frame = self.original.get_frame()

            # If sizes does not match, resize frame
            if self.original.height != self.height or self.original.width != self.width:
                new_frame = cv2.resize(new_frame, (self.width, self.height))

            # Set Frame Size
            self.set_frame(new_frame)
            self.frame_controller.next_frame()
