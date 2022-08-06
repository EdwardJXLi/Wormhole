from wormhole.viewer.socketioviewer import SocketIOViewerBase

import numpy as np
import cv2

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


# Viewer for all types of image formats supported by imdecode  
class RawIMDecodeViewerBase(SocketIOViewerBase):
    def __init__(
        self, 
        *args,
        **kwargs
    ):
        # Initiate Parent SocketIO Viewer Object
        super().__init__(self.raw_image_handler, *args, **kwargs)

    # Create Handler for Incoming Raw Data Frames
    def raw_image_handler(self, raw):
        np_image = np.fromstring(raw, dtype=np.uint8)  # type: ignore
        new_frame = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
        self.set_frame(new_frame)

# Proxy classes for each of the supported streaming formats. 
# They all run the exact same thing, but this is here so it fits with the API structure


# Viewer for Raw JPEG Streaming
class RawJPEGViewer(RawIMDecodeViewerBase):
    def __init__(
        self, 
        *args,
        **kwargs
    ):
        # Initiate Parent SocketIO Viewer Object
        super().__init__(*args, **kwargs)
        
        
# Viewer for Raw PNG Streaming
class RawPNGViewer(RawIMDecodeViewerBase):
    def __init__(
        self, 
        *args,
        **kwargs
    ):
        # Initiate Parent SocketIO Viewer Object
        super().__init__(*args, **kwargs)


# Viewer for Raw Image Format Streaming
class RawImageFormatViewer(RawIMDecodeViewerBase):
    def __init__(
        self, 
        image_format,
        *args,
        **kwargs
    ):
        # Image Format isnt used, but keeping it here for API compatibility.
        self.image_format = image_format
        # Initiate Parent SocketIO Viewer Object
        super().__init__(*args, **kwargs)
