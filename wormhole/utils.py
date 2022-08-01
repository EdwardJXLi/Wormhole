import time
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
    def __init__(self, fps: int, print_fps: bool = False):
        # Core Functionality
        self.target_fps: int = fps
        self.last_frame: float = time.time()
        # Sanity Checks for FPS
        self.print_fps = print_fps
        self.start_time = time.time()
        self.frames_rendered = 0
        self.actual_fps = 0
    
    def get_sleep_time(self):
        cur_time = time.time()
        time_elapsed = cur_time - self.last_frame
        return max((1. / self.target_fps) - time_elapsed, 0.0)
    
    def next_frame(self):
        # Ensure FPS
        time.sleep(self.get_sleep_time())
        self.last_frame = time.time()
        # Calculate FPS
        self.frames_rendered += 1
        self.actual_fps = self.frames_rendered / (time.time() - self.start_time)
        if self.print_fps:
            print("Frame Rate", self.actual_fps)
            
    def reset_fps_stats(self):
        self.__init__(self.target_fps, self.print_fps)
