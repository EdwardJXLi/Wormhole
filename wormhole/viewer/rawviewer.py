from wormhole.viewer import AbstractViewer
from wormhole.utils import FrameController

from threading import Thread
from urllib.parse import urlparse
import cv2
import socketio
import numpy as np

# Base Class for Viewing All Raw Image Streaming Formats   
class RawViewerBase(AbstractViewer):
    def __init__(
        self, 
        encode_format: str,
        url: str, 
        height: int, 
        width: int, 
        max_fps: int = 30, 
        *args,
        **kwargs
    ):
        # Save basic variables about stream
        self.encode_format = encode_format
        parsed_url = urlparse(url)
        self.hostname = f"{parsed_url.scheme}://{parsed_url.netloc}"
        self.namespace = parsed_url.path
        
        # Setup SocketIO Client
        self.sio_client = socketio.Client(*args, **kwargs)
        
        # Initiate Video Parent Object
        super().__init__(height, width, max_fps=max_fps)
        
        # Create Handler for Incoming Images
        def raw_image_handler(raw):
            np_image = np.fromstring(raw, dtype=np.uint8)  # type: ignore
            i = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
            self.set_frame(i)
        
        # Create SocketIO Handler for when raw images stream in
        self.sio_client.on("video_frame", raw_image_handler, namespace=self.namespace)
        
        # Connect To Server
        self.sio_client.connect(self.hostname, namespaces=[self.namespace])

# Below are the different image encoding types the system supports
# NOTE: The encode format doesnt actually do anything for the viewer, as imdecode figures it out itself, but its just here for reference
 
# Raw JPEG Viewer
class RawJPEGViewer(RawViewerBase):
    def __init__(self, *args, **kwargs):
        super().__init__(".jpg", *args, **kwargs)
        
