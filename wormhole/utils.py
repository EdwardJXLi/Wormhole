import time

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
