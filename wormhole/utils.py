import time
import math
import numpy as np

# Helper functions to render colors
# Set the current frame to a blank frame with a given color
def blank_frame_color(height:int, width:int, color: tuple):
    new_frame = np.zeros((height, width, 3), np.uint8)
    new_frame[:,:,:] = color
    return new_frame
    
# Set the current frame to a blank frame with a given color
def blank_frame_color_rgb(height:int, width:int, r: int, g: int, b: int):
    new_frame = np.zeros((height, width, 3), np.uint8)
    new_frame[:,:,:] = (r, g, b)
    return new_frame

# Helper Class to Control Video Frame Rate
class FrameController():
    def __init__(self, fps: int, print_fps: bool = False, sleep_func = None, fps_window_delta: float = 5.0):
        # Core Functionality
        self.target_fps: int = fps
        self.last_frame: float = time.time()
        self.frame_time: float = 0.0
        # Sanity Checks for FPS
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
        # Sleep Function is used for if a specific non-blocking sleep function is needed.
        # Gevent Patches already do this, so its not that necessary, but keeping it here for compatibility.
        self.sleep_func = sleep_func or time.sleep
    
    def get_sleep_time(self):
        cur_time = time.time()
        self.frame_time = cur_time - self.last_frame
        return max((1. / self.target_fps) - self.frame_time, 0.0)
    
    def next_frame(self):
        # Ensure FPS
        self.sleep_func(self.get_sleep_time())
        self.last_frame = time.time()
        # Calculate Instantaneous FPS
        instantaneous_fps = 1.0 / self.frame_time
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
            print("Instantaneous FPS: {0:.2f} Average FPS: {1:.2f} Windowed FPS: {2:.2f} Frame Time {3:.2f} ms".format(
                instantaneous_fps, self.average_fps, self.fps_window, self.frame_time*1000
            ))
            
    def reset_fps_stats(self):
        self.__init__(self.target_fps, self.print_fps)
