from wormhole.viewer import AbstractViewer

import math
import socketio
from typing import Callable, Optional
from urllib.parse import urlparse


class SocketIOViewerBase(AbstractViewer):
    """
    Base Class for Everything SocketIO Viewer
    """

    def __init__(
        self,
        data_processor: Callable,
        url: str,
        width: int,
        height: int,
        max_fps: float = math.inf,
        socketio_args: Optional[dict] = None,
        **kwargs
    ):
        # Save basic variables about stream
        parsed_url = urlparse(url)
        self.hostname = f"{parsed_url.scheme}://{parsed_url.netloc}"
        self.namespace = parsed_url.path

        # Save Raw Data Processing Function
        self.data_processor = data_processor

        # Setup SocketIO Client
        self.sio_client = socketio.Client(**socketio_args if socketio_args else {})

        # Initiate Video Parent Object
        super().__init__(width, height, max_fps=max_fps, **kwargs)

        # Create SocketIO Handler for when raw images stream in
        # Proxying the function with a lambda so that the self context is also passed in
        self.sio_client.on("frame", self.data_processor, namespace=self.namespace)

        # Connect To Server
        self.sio_client.connect(self.hostname, namespaces=[self.namespace])
