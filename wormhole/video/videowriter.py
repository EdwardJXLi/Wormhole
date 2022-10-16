from wormhole.utils import FrameController
from wormhole.video import AbstractVideo

import cv2
from typing import Optional
import logging


def write_video(
    video: AbstractVideo,
    filename: str,
    encoding: Optional[str | tuple | int] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    max_fps: Optional[float] = None,
    print_fps: bool = False
):
    width = width or video.width
    height = height or video.height
    max_fps = max_fps or video.max_fps
    frame_controller = FrameController(max_fps, print_fps=print_fps)
    
    # Get File Encoding Format
    if isinstance(encoding, int):
        fourcc = encoding
    elif isinstance(encoding, tuple) or isinstance(encoding, str):
        fourcc = cv2.VideoWriter_fourcc(*encoding)
    else:
        logging.warning("No encoding format specified. Automatically determining encoding format.")
        fourcc = -1
    
    # Create File Writer Object
    video_writer = cv2.VideoWriter(filename, fourcc, max_fps, (width, height))
    
    # Sanity Check
    if not video_writer.isOpened():
        raise Exception("Video Writer Failed to Initialize!")
    
    while True:
        # Sanity Check
        if not video_writer.isOpened():
            raise Exception("Video Writer Suddenly Failed!")
        
        # Get the next frame
        frame = video.get_frame()
        
        # Resize frame or else the video will break
        frame = cv2.resize(frame, (width, height))
        
        # Write the frame to file
        video_writer.write(frame)
        frame_controller.next_frame()

    # This never gets called...
    # video_writer.release()

# Some predefined fourcc codes
H264_CODEC = cv2.VideoWriter_fourcc('H', '2', '6', '4')
H265_CODEC = cv2.VideoWriter_fourcc('H', 'E', 'V', 'C')
MPEG4_CODEC = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
XVID_CODEC = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
MJPG_CODEC = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
X264_CODEC = cv2.VideoWriter_fourcc('X', '2', '6', '4')
VP8_CODEC = cv2.VideoWriter_fourcc('V', 'P', '8', '0')
VP9_CODEC = cv2.VideoWriter_fourcc('V', 'P', '9', '0')
AV1_CODEC = cv2.VideoWriter_fourcc('A', 'V', '0', '1')
