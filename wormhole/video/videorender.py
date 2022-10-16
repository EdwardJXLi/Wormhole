from wormhole.utils import FrameController
from wormhole.video import AbstractVideo

import cv2
from typing import Optional


def render_video(
    video: AbstractVideo,
    width: Optional[int] = None,
    height: Optional[int] = None,
    max_fps: Optional[float] = None,
    print_fps: bool = False,
    window_name="Video Preview"
):
    # Basic Video Information
    width = width or video.width
    height = height or video.height
    max_fps = max_fps or video.max_fps
    frame_controller = FrameController(max_fps, print_fps=print_fps)
    
    # Hot loop for video rendering
    while True:
        frame = video.get_frame()
        cv2.imshow(window_name, cv2.resize(frame, (width, height)))
        # Check if q is sent to exit video
        if cv2.waitKey(1) == ord('q'):
            break
        frame_controller.next_frame()
    
    # Safely clean all windows
    cv2.destroyAllWindows()
