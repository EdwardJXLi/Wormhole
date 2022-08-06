from wormhole.streamer.socketiostreamer import SocketIOStreamerBase

import cv2
from typing import Optional, Any


class RawStreamer(SocketIOStreamerBase):
    """
    Raw Image Streaming
    This is generally not recommended as it sends A LOT of information over the network, 
    But its an interesting experiment to see the maximum processing throughput
    Without any image encoding
    """

    def __init__(
        self,
        *args,
        **kwargs
    ):
        # Initiate Parent SocketIO Streamer Object
        super().__init__(self.stream_hotloop, *args, **kwargs)

    # Hotloop for sending raw video
    def stream_hotloop(self):
        self.send_data(self.video.get_frame().tobytes())


class RawIMEncodeStreamerBase(SocketIOStreamerBase):
    """
    Streamer for all types of image formats supported by imencode  
    """

    def __init__(
        self,
        file_format: str,
        *args,
        imencode_config: Optional[list[Any]] = None,
        **kwargs
    ):
        # Initiate Parent SocketIO Streamer Object
        super().__init__(self.stream_hotloop, *args, **kwargs)

        # Setup some configs for the imencode function
        self.file_format = file_format
        self.imencode_config = imencode_config

    # Hotloop for sending raw video
    def stream_hotloop(self):
        _, encoded_image = cv2.imencode(
            self.file_format,
            self.video.get_frame(),
            self.imencode_config or []  # Use Empty Config if imencode is not available
        )
        self.send_data(encoded_image.tobytes())

# Proxy classes for each of the supported streaming formats.
# They all run the exact same thing, but this is here so it fits with the API structure


class RawJPEGStreamer(RawIMEncodeStreamerBase):
    """
    Raw JPEG Streaming
    Sends raw individual PNG frames over the network
    """

    def __init__(
        self,
        *args,
        **kwargs
    ):
        super().__init__(".jpeg", *args, **kwargs)


class RawPNGStreamer(RawIMEncodeStreamerBase):
    """
    Raw PNG Streaming
    Sends raw individual PNG frames over the network
    """

    def __init__(
        self,
        *args,
        **kwargs
    ):
        super().__init__(".png", *args, **kwargs)


class RawImageFormatStreamer(RawIMEncodeStreamerBase):
    """
    Raw Image File Streaming
    Sends raw individual image file frames over the network
    """

    def __init__(
        self,
        image_format,
        *args,
        **kwargs
    ):
        super().__init__(image_format, *args, **kwargs)
