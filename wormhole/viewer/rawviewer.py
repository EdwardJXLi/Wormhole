from wormhole.viewer.socketioviewer import SocketIOViewerBase

import numpy as np

# Viewer for Raw Image Streaming  
class RawViewer(SocketIOViewerBase):
    def __init__(
        self, 
        *args,
        **kwargs
    ):
        # Initiate Parent SocketIO Viewer Object
        super().__init__(self.raw_image_handler, *args, **kwargs)
        
    # Create Handler for Incoming Raw Data Frames
    def raw_image_handler(self, raw):
        new_frame = np.ndarray((self.width, self.height, 3), np.uint8, raw)
        self.set_frame(new_frame)
        
