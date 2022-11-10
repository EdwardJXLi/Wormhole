import cv2
import math
import numpy as np
import time
from pathlib import Path
from typing import Union


#
# --- Helper functions to render colors, text, and images ---
#


def blank_frame_color(width: int, height: int, color: tuple, pixel_size: int = 3):
    """
    Set the current frame to a blank frame with a given color
    """

    new_frame = np.zeros((height, width, pixel_size), np.uint8)
    new_frame[:, :, :] = color
    return new_frame


def blank_frame_color_rgb(width: int, height: int, r: int, g: int, b: int, pixel_size: int = 3):
    """
    Set the current frame to a blank frame with a given color
    """

    new_frame = np.zeros((height, width, pixel_size), np.uint8)
    new_frame[:, :, :] = (r, g, b)
    return new_frame


def draw_text(
    frame: np.ndarray,
    text: str,
    position: tuple[int, int],
    font_family: int = cv2.FONT_HERSHEY_SIMPLEX,
    font_size: float = 1,
    font_color: tuple = (255, 255, 255),
    font_stroke: int = 2
):
    """
    Draws text at given location
    """

    return cv2.putText(
        frame,
        text,
        position,
        font_family,
        font_size,
        font_color,
        font_stroke
    )


def draw_multiline_text(
    frame: np.ndarray,
    width: int,
    height: int,
    position: tuple[int, int],
    text: Union[str, list[str]]
):
    """
    Helper function to draw multiple lines of text at once. Automatically determines ideal rendering size
    """

    # Parse the text input
    if type(text) is str:
        text = [text]

    # Disable this feature for now.
    '''
    # Determine Information On Rendered Text
    CHAR_WIDTH, CHAR_HEIGHT = 30, 30
    FONT_SIZE = 1
    FONT_STROKE = 2
    num_lines = len(text)
    max_width = max(len(l) for l in text)

    # Check if the text will fit on the screen. If not, zoom out
    if max_width * CHAR_WIDTH < width and num_lines * CHAR_HEIGHT < height:
        pass
    else:
        # Does not fit. Change text size
        CHAR_WIDTH, CHAR_HEIGHT = 15, 15
        FONT_SIZE = 0.5
        FONT_STROKE = 1
    '''
    
    # Break down position
    x_offset, y_offset = position
    
    # Always use zoomed out mode
    CHAR_HEIGHT = 18
    FONT_SIZE = 0.5
    FONT_STROKE = 1    

    # Place the text on the frame
    for i, line in enumerate(text):
        frame = draw_text(frame, line, (x_offset + 10, y_offset + (i + 1) * CHAR_HEIGHT), font_size=FONT_SIZE, font_stroke=FONT_STROKE)

    return frame


def draw_overlay(frame, overlay_image, position: tuple[int, int], overlay_size: tuple[int, int]):
    """
    Draws a solid image ontop of another imge
    """
    
    # Extract the positions
    pos_x, pos_y = position
    
    # Extract the size
    overlay_width, overlay_height = overlay_size

    # If sizes does not match, resize frame
    frame_height, frame_width, _ = overlay_image.shape
    if (frame_width, frame_height) != overlay_size:
        overlay_image = cv2.resize(overlay_image, overlay_size)
        
    frame[pos_y:pos_y+overlay_height, pos_x:pos_x+overlay_width] = overlay_image
    
    return frame


def draw_transparent_overlay(frame, overlay_image, position: tuple[int, int], overlay_size: tuple[int, int]):
    """
    Overlay an image with a transparency layer onto a frame
    Code adapted from: https://gist.github.com/clungzta/b4bbb3e2aa0490b0cfcbc042184b0b4e
    """
    # Extract the positions
    pos_x, pos_y = position

    # If sizes does not match, resize frame
    frame_height, frame_width, _ = overlay_image.shape
    if (frame_width, frame_height) != overlay_size:
        overlay_image = cv2.resize(overlay_image, overlay_size)

    # Extract the alpha mask of the RGBA image, convert to RGB
    b, g, r, a = cv2.split(overlay_image)
    overlay_color = cv2.merge((b, g, r))

    # Apply some simple filtering to remove edge noise
    mask = cv2.medianBlur(a, 5)

    h, w, _ = overlay_color.shape
    roi = frame[pos_y:pos_y + h, pos_x:pos_x + w]

    # Black-out the area behind the logo in our original ROI
    img1_bg = cv2.bitwise_and(roi.copy(), roi.copy(), mask=cv2.bitwise_not(mask))

    # Mask out the logo from the logo image.
    img2_fg = cv2.bitwise_and(overlay_color, overlay_color, mask=mask)

    # Update the original image with our new ROI
    frame[pos_y:pos_y + h, pos_x:pos_x + w] = cv2.add(img1_bg, img2_fg)

    return frame


def blend_frames(frame1: np.ndarray, frame2: np.ndarray, transparency=0.5):
    """
    Blends two frames together with a transparency value
    """

    # Render the image onto the overlay
    # Draw image over frame with transparency
    cv2.addWeighted(frame2, transparency, frame1, 1 - transparency, 0, frame1)
    return frame1


#
# --- Frame Modifiers to render watermark ---
#


def render_watermark(video):
    """
    Renders a "Powered By Wormhole" watermark at the bottom of the screen
    """

    # Checks if loaded image is already in cache
    wormhole_watermark = globals().get("wormhole_watermark")
    if wormhole_watermark is None:
        # Load the image
        BASE = Path(__file__).parent
        wormhole_watermark = cv2.imread(str(Path(BASE, "assets", "poweredby_white.png")), -1)

        # Cache the image
        globals()["wormhole_watermark"] = wormhole_watermark

    # Dynamically determine the watermark padding distance
    padding = max(video.height // 50, video.width // 50)

    # --- Calculate the watermark position ---

    # Get watermark height and width
    wm_height, wm_width = wormhole_watermark.shape[:2]

    # Get target width and height
    target_width = video.width // 1.5
    target_height = video.height // 6

    # Get ratios of the two targets, and calculate which one is smaller
    width_ratio = target_width / wm_width
    height_ratio = target_height / wm_height
    ratio = min(width_ratio, height_ratio)

    # Get the proper widths and heights
    width = int(wm_width * ratio)
    height = int(wm_height * ratio)

    # Render the watermark onto a copy of the frame
    watermarked_frame = draw_transparent_overlay(video._frame.copy(), wormhole_watermark, (padding, video.height - height - padding), (width, height))

    # Render the watermark with the new width and height
    blend_frames(video._frame, watermarked_frame)

#
# --- Frame Modifiers to render fps and other statistics ---
#


def render_fps(video):
    """
    Render the current fps on the current frame
    """

    # Render the fps
    draw_text(video._frame, f"FPS: {video.frame_controller.average_fps}", (10, 30))


def render_fraps_fps(video):
    """
    Render the current fps in the top right corner like fraps
    """

    # Get the fps
    fps = str(int(min(video.frame_controller.average_fps, 0)))  # Fixes a small bug with inf fps
    # Render the fps
    draw_text(video._frame, f"{fps}", (video.width - len(fps) * 20 - 10, 30), font_color=(0, 0, 0), font_stroke=6)
    draw_text(video._frame, f"{fps}", (video.width - len(fps) * 20 - 10, 30), font_color=(0, 255, 255))


def render_full_fps(video):
    """
    Renders full FPS statistics on the current frame. Includes: Frame Time, Instantaneous FPS, FPS over X seconds, and Average FPS
    """

    # Render the fps
    draw_multiline_text(video._frame, video.width, video.height, (0, 0), [
        f"Frame Time: {video.frame_controller.frame_time * 1000:.2f} ms",
        f"Instantaneous FPS: {video.frame_controller.instantaneous_fps:.2f}",
        f"FPS over {video.frame_controller.fps_window_delta:.1f} Seconds: {video.frame_controller.fps_window:.2f}",
        f"Average FPS: {video.frame_controller.average_fps:.2f}"
    ])


def render_debug_info(video):
    """
    Renders full debug information about the video stream
    """

    # Render the fps
    from wormhole.version import __version__
    draw_multiline_text(video._frame, video.width, video.height, (0, 0), [
        f"=== [Debug Information] ===",
        f"Wormhole Version: {__version__}",
        f">>> Video Information <<<",
        f"Render Source: {type(video).__name__}",
        f"Height: {video.height} | Width: {video.width} | Pixel Size: {video.pixel_size}",
        f"Maximum Render FPS: {video.max_fps}",

        f">>> Frame Rate Information <<<",
        f"Frame Time: {video.frame_controller.frame_time * 1000:.2f} ms",
        f"Instantaneous FPS: {video.frame_controller.instantaneous_fps:.2f}",
        f"FPS over {video.frame_controller.fps_window_delta:.1f} Seconds: {video.frame_controller.fps_window:.2f}",
        f"Average FPS: {video.frame_controller.average_fps:.2f}",
        f"Frames Rendered: {video.frame_controller.frames_rendered}",

        f">>> Frame Modifiers <<<",
        *[str(modifier) for modifier in video.frame_modifiers],
        f">>> Frame Subscribers <<<",
        *[str(subscriber) for subscriber in video.frame_subscribers],

        f"=== [Debug Information] ===",
    ])


#
# --- Additional Frame Modifiers to modify image ---
#


def grayscale_filter(video):
    """
    Makes video black and white
    """

    cv2.cvtColor(video._frame, cv2.COLOR_BGR2GRAY)
    cv2.cvtColor(video._frame, cv2.COLOR_GRAY2BGR)


def inverse_filter(video):
    """
    Inverts all colors in the video
    """

    cv2.bitwise_not(video._frame)


#
# --- Helper Classes ---
#


class FrameController():
    """
    Helper Class to Control Video Frame Rate
    """

    def __init__(self, fps: float, print_fps: bool = False, sleep_func=None, fps_window_delta: float = 5.0):
        # --- Core Functionality ---
        if fps <= 0.0:
            raise ValueError("FPS must be greater than 0!")

        self.target_fps: float = fps
        self.last_frame: float = time.time()
        self.frame_time: float = 0.0

        # --- Sanity Checks for FPS ---

        # Instantaneous FPS
        self.instantaneous_fps: float = math.inf
        # Average FPS
        self.print_fps: bool = print_fps
        self.start_time: float = time.time()
        self.frames_rendered: int = 0
        self.average_fps: float = math.inf
        # Windowed FPS (FPS over X seconds)
        self.fps_window_delta: float = fps_window_delta
        self.fps_window_start: float = time.time()
        self.fps_window_frames_rendered: int = 0
        self.fps_window: float = math.inf

        # --- Misc Stuff ---

        # Sleep Function is used for if a specific non-blocking sleep function is needed.
        # Gevent Patches already do this, so its not that necessary, but keeping it here for compatibility.
        self.sleep_func = sleep_func or time.sleep

    def get_sleep_time(self):
        cur_time = time.time()
        self.frame_time = cur_time - self.last_frame
        return max((1. / self.target_fps) - self.frame_time, 0.0)

    def next_frame(self):
        # Ensure FPS
        sleep_time = self.get_sleep_time()
        if sleep_time:  # Save on the expensive sleep function is no sleep is needed
            self.sleep_func(sleep_time)
        self.last_frame = time.time()
        # Update FPS Counter
        self.update_fps()

    def update_fps(self):
        # Calculate Instantaneous FPS
        if self.frame_time != 0.0:  # Fix bug where frame is so fast that it divides by zero
            self.instantaneous_fps = 1.0 / self.frame_time
        else:
            self.instantaneous_fps = math.inf
        # Calculate Total Average FPS
        self.frames_rendered += 1
        self.average_fps = self.frames_rendered / (time.time() - self.start_time)
        # Calculate Windowed FPS
        self.fps_window_frames_rendered += 1
        if time.time() - self.fps_window_start > self.fps_window_delta:
            self.fps_window = self.fps_window_frames_rendered / (time.time() - self.fps_window_start)
            self.fps_window_frames_rendered = 0
            self.fps_window_start = time.time()
        # Print FPS
        if self.print_fps:
            print(f"Instantaneous FPS: {self.instantaneous_fps:.2f} Average FPS: {self.average_fps:.2f} FPS over {self.fps_window_delta:.1f} Seconds: {self.fps_window:.2f} Frame Time {self.frame_time * 1000:.2f} ms")

    def reset_fps_stats(self):
        self.__init__(self.target_fps, self.print_fps, sleep_func=self.sleep_func, fps_window_delta=self.fps_window_delta)
