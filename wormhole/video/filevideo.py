from wormhole.utils import FrameController
from wormhole.video import AbstractVideo

import cv2
from pathlib import Path
from threading import Thread
from typing import Any, Optional


class FileVideo(AbstractVideo):
    """
    Creates a video object from a video file
    """

    def __init__(
        self,
        filename: str,
        max_fps: Optional[float] = 30,
        width: Optional[int] = None,
        height: Optional[int] = None,
        repeat: bool = True,
        cv2_config: Optional[list[tuple[Any, Any]]] = None,
        **kwargs  # Any Additional Arguments for AbstractVideo
    ):
        # Basic Video Properties
        self.filename: str = filename
        # Optional Video Properties
        self.repeat: bool = repeat

        # Check if file exists
        if not Path(self.filename).exists():
            raise Exception(f"File {self.filename} Does Not Exist!")

        # Open Video File
        self.cap = cv2.VideoCapture(self.filename)

        # Check if video open was successful
        if self.cap is None or not self.cap.isOpened():
            raise ValueError(f"Video Not Opened! Something went wrong!")

        # Set CV2 Settings
        if cv2_config:
            for key, value in cv2_config:
                self.cap.set(key, value)
        # Set width, height, or fps if they are not set by default
        max_fps = max_fps or int(self.cap.get(cv2.CAP_PROP_FPS))
        width = width or int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = height or int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Initialize Video Object
        super().__init__(width, height, max_fps, **kwargs)

        # Check if Video File Opened
        if not self.cap.isOpened():
            raise ValueError("Video File Not Opened! An Error Probably Occurred.")
        # Set up Frame Controller
        self.frame_controller = FrameController(self.max_fps, print_fps=self.print_fps)

        # Start Video Thread
        self.video_thread = Thread(target=self.video_loop, daemon=True)
        self.video_thread.start()

    def video_loop(self):
        # Start Video Loop
        while True:
            try:
                # Read Frame
                ret, frame = self.cap.read()
                # Check if Frame is Valid
                if not ret:
                    if self.repeat:
                        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    else:
                        self.set_blank_frame()
                    continue

                # If sizes does not match, resize frame
                frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                if frame_width != self.width or frame_height != self.height:
                    frame = cv2.resize(frame, (self.width, self.height))

                # Set Frame
                self.set_frame(frame)
                self.frame_controller.next_frame()
            except Exception as e:
                self.handle_render_error(e, message="Error While Rendering Video File!")
