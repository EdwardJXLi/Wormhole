import time

# Helper Class to Control Video Frame Rate
class FrameController():
    def __init__(self, fps: int):
        self.fps: int = fps
        self.last_frame: float = time.time()
        self.start_time = time.time()
        self.frames_rendered = 0
    
    def next_frame(self):
        cur_time = time.time()
        time_elapsed = cur_time - self.last_frame
        s = max((1. / self.fps) - time_elapsed, 0.0)
        time.sleep(s)
        self.last_frame = time.time()
        self.frames_rendered += 1
        print("Frame Rate", self.frames_rendered / (time.time() - self.start_time))
