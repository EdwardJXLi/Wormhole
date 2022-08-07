from wormhole.viewer import SocketIOViewerBase

import cv2
import numpy as np


class RawViewer(SocketIOViewerBase):
    """
    Viewer for Raw Image Streaming
    """

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
            raise Exception(f"Invalid frame size! Expected: {self.width * self.height * 3} bytes but received: {raw} bytes!")

        # Convert 1d data array to 3d frame data
        new_frame = np.ndarray((self.width, self.height, 3), np.uint8, raw)

        # New Frame!
        self.set_frame(new_frame)


class RawIMDecodeViewerBase(SocketIOViewerBase):
    """
    Viewer for all types of image formats supported by imdecode
    """

    def __init__(
        self,
        *args,
        **kwargs
    ):
        # Initiate Parent SocketIO Viewer Object
        super().__init__(self.raw_image_handler, *args, **kwargs)

    # Create Handler for Incoming Raw Data Frames
    def raw_image_handler(self, raw):
        # Read and decode data
        np_image = np.fromstring(raw, dtype=np.uint8)  # type: ignore
        new_frame = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

        # If sizes does not match, resize frame
        frame_width, frame_height, _ = new_frame.shape
        if frame_width != self.width or frame_height != self.height:
            new_frame = cv2.resize(new_frame, (self.width, self.height))

        # Set the new frame
        self.set_frame(new_frame)

# Proxy classes for each of the supported streaming formats.
# They all run the exact same thing, but this is here so it fits with the API structure


class RawJPEGViewer(RawIMDecodeViewerBase):
    """
    Viewer for Raw JPEG Streaming
    """

    def __init__(
        self,
        *args,
        **kwargs
    ):
        # Initiate Parent SocketIO Viewer Object
        super().__init__(*args, **kwargs)


class RawPNGViewer(RawIMDecodeViewerBase):
    """
    Viewer for Raw PNG Streaming
    """

    def __init__(
        self,
        *args,
        **kwargs
    ):
        # Initiate Parent SocketIO Viewer Object
        super().__init__(*args, **kwargs)


class RawImageFormatViewer(RawIMDecodeViewerBase):
    """
    Viewer for Raw Image Format Streaming
    """

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
