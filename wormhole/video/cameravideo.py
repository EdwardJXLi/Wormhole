from wormhole.utils import FrameController
from wormhole.video import AbstractVideo

import cv2
from threading import Thread
from typing import Any, Optional


class CameraVideo(AbstractVideo):
    """
    Creates a video object from a camera
    """

    def __init__(
        self,
        cam_id: int,
        max_fps: Optional[float] = 30,
        width: Optional[int] = None,
        height: Optional[int] = None,
        cv2_config: Optional[list[tuple[Any, Any]]] = None,
        **kwargs  # Any Additional Arguments for AbstractVideo
    ):
        # Basic Video Properties
        self.cam_id: int = cam_id

        # Open Camera
        self.cap = cv2.VideoCapture(self.cam_id)
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

        # Check if Camera Opened Successfully
        if not self.cap.isOpened():
            raise ValueError("Camera Not Opened! An Error Probably Occurred.")
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
                _, frame = self.cap.read()

                # If sizes does not match, resize frame
                frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                if frame_width != self.width or frame_height != self.height:
                    frame = cv2.resize(frame, (self.width, self.height))

                # Set Frame
                self.set_frame(frame)
                self.frame_controller.next_frame()
            except Exception as e:
                self.handle_render_error(e, message="Error While Capturing Camera Frame!")
