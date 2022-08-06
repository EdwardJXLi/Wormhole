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
        # Sanity Check for Stream Info
        if len(raw) != self.width * self.height * 3:
            raise Exception(f"Invalid frame size! Expected: {self.width * self.height * 3} bytes but received: {raw} bytes! This is most likely because the width and height send by the server are modified from source!")
        
        # Convert 1d data array to 3d frame data
        new_frame = np.ndarray((self.width, self.height, 3), np.uint8, raw)
        
        # New Frame!
        self.set_frame(new_frame)
        
