from wormhole.viewer import AbstractViewer

import cv2
import urllib.request
import numpy as np
import traceback
import threading

# Viewer for the Motion JPEG video protocol
class MJPEGViewer(AbstractViewer):
    def __init__(self, url: str, height: int, width: int, max_fps: int = 30):
        # Save basic variables about stream
        self.url = url
        
        # Start the video decoder in another thread
        self.video_decoder_thread = threading.Thread(target=self.video_decoder)
        self.video_decoder_thread.daemon = True
        self.video_decoder_thread.start()
        
        super().__init__(height, width, max_fps=max_fps)
        
    def video_decoder(self):
        while True:
            try:
                with urllib.request.urlopen(self.url) as stream:
                    inBytes = bytes()
                    while True:
                        inBytes += stream.read(1024)
                        a = inBytes.find(b'\xff\xd8')
                        b = inBytes.find(b'\xff\xd9')
                        if a != -1 and b != -1:
                            jpg = inBytes[a:b+2]
                            inBytes = inBytes[b+2:]
                            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)  # type: ignore
                            print(type(i))
                            self.set_frame(i)
            except Exception as e:
                print(f"Open Camera Error: {e}")
                traceback.print_exc()
        
