from wormhole.viewer import AbstractViewer

import math
import socketio
from typing import Callable
from urllib.parse import urlparse


class SocketIOViewerBase(AbstractViewer):
    """
    Base Class for Everything SocketIO Viewer
    """

    def __init__(
        self,
        data_processor: Callable,
        url: str,
        height: int,
        width: int,
        max_fps: float = math.inf,
        print_fps: bool = False,
        *args,
        **kwargs
    ):
        # Save basic variables about stream
        parsed_url = urlparse(url)
        self.hostname = f"{parsed_url.scheme}://{parsed_url.netloc}"
        self.namespace = parsed_url.path

        # Save Raw Data Processing Function
        self.data_processor = data_processor

        # Setup SocketIO Client
        self.sio_client = socketio.Client(*args, **kwargs)

        # Initiate Video Parent Object
        super().__init__(height, width, max_fps=max_fps, print_fps=print_fps)

        # Create SocketIO Handler for when raw images stream in
        # Proxying the function with a lambda so that the self context is also passed in
        self.sio_client.on("frame", self.data_processor, namespace=self.namespace)

        # Connect To Server
        self.sio_client.connect(self.hostname, namespaces=[self.namespace])
