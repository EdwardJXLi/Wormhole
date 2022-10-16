from wormhole.utils import FrameController
from wormhole.video import AbstractVideo

from pathlib import Path
from typing import Optional
import cv2
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
        # Autodetect File Encoding
        suffix = Path(filename).suffix
        if suffix == ".mp4":
            # NOTE: h264 is not supported everywhere
            # fourcc = cv2.VideoWriter_fourcc(*"h264")
            fourcc = cv2.VideoWriter_fourcc(*"MP4V")
        elif suffix == ".avi":
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
        elif suffix == ".webm":
            # NOTE: VP9 is wayyy to buggy for handling unstable video
            # fourcc = cv2.VideoWriter_fourcc(*"VP90")
            fourcc = cv2.VideoWriter_fourcc(*"VP80")
        else:
            # TODO: Potentially support more codecs and formats in the future?
            logging.warning("Unknown File Encoding Format. Using OepnCV Default.")
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
