__version__ = "development"
from gevent import monkey
monkey.patch_all()
from typing import Type, Optional
# from multiprocessing import Process
from threading import Thread
from flask import request

from wormhole.video import AbstractVideo
from wormhole.controller import AbstractController, FlaskController
from wormhole.streamer import AbstractStreamer
from wormhole.viewer import AbstractViewer

# Entrypoint for everything WORMHOLE!
class Wormhole():
    def __init__(
        self, 
        # Basic Controller Settings
        network_controller: Type[AbstractController] = FlaskController,
        # Advanced Controller Settings
        # Extra Features
        welcome_screen: bool = True,
        advanced_features: bool = True,
        supported_protocols: Optional[
            dict[
                str, 
                tuple[
                    Type[AbstractStreamer], 
                    Type[AbstractViewer]
                ]
            ]
        ] = None,
        # Pass All Other Arguments to the Controller
        *args,
        **kwargs
    ):
        # Create Controller
        self.controller = network_controller(self, *args, **kwargs)
        
        # Set Up Streamers
        # List of streamers with the route as they key and the streamer object as the value
        self.routes: dict[str, AbstractStreamer] = {}
        # List of automatically managed streams with the video name as the key
        # The value is a tuple with the stream object and the list of supported protocols
        self.managed_streams: dict[str, tuple[AbstractVideo, list[str]]] = {}
            
        # Set up advanced Wormhole features
        self.advanced_features = advanced_features
        from wormhole.streamer.mjpegstreamer import MJPEGStreamer
        from wormhole.viewer.mjpegviewer import MJPEGViewer
        self.supported_protocols = supported_protocols or {  
            # ORDER MATTERS HERE! Ranked in order from most preferred to least preferred!
            "MJPEG": (MJPEGStreamer, MJPEGViewer),
        }
        if self.advanced_features:
            self.set_up_advanced_features()
        
        # Set up welcome screen
        if welcome_screen:
            def hello_world():
                return (
                    "<h1>Welcome to Wormhole!</h1>"
                    "<h3>If you see this page, Wormhole Video Streaming Server is successfully installed and working!</h3>"
                    f"<p>Version: {__version__}</p>"
                )
            self.controller.add_route("/", hello_world, strict_slashes=False)
            
        # Start Server In Another Thread
        self.wormhole_thread = Thread(target=self.controller.start_server, daemon=True)
        self.wormhole_thread.start()
        
    def set_up_advanced_features(self):
        # Set up basic client sync
        def client_sync():
            # Get client information
            client = request.json
            if not client:
                return "Invalid Json!", 400
            if "version" not in client or "supported_protocols" not in client:
                return "Json Missing Fields!", 400
            
            # Check if versions match
            client_version = client.get("version", "N/A")
            if client_version != __version__:
                return f"Wormhole Version Mismatch! Server: {__version__} Client: {client_version}", 400
            
            # Get client supported protocols
            # Not really useful for now, but we will parse it anyways
            client_supported_protocols = client.get("supported_protocols", [])
            
            # Return with server information
            server_response = {
                "version": __version__,
                "ready": True,
                "supported_protocols": list(self.supported_protocols.keys()),
                "managed_streams": list(self.managed_streams.keys()),
            }
            
            return server_response, 200
        self.controller.add_route("/wormhole/sync", client_sync, methods=["POST"], strict_slashes=False, ignore_url_check=True)
        
        # Set Up Stream Sync
        def stream_sync(name):
            if name not in self.managed_streams:
                return "Stream Not Found!", 404
            
            # Get Stream Information
            video_obj, supported_protocols = self.managed_streams[name]
            
            # Return with server information
            server_response = {
                "version": __version__,
                "camera_name": name,
                "supported_protocols": supported_protocols,
                "stream_info": {
                    "width": video_obj.width,
                    "height": video_obj.height,
                    "max_fps": video_obj.max_fps
                }
            }
            
            return server_response, 200
        self.controller.add_route("/wormhole/stream/<name>/sync", stream_sync, methods=["GET", "POST"], strict_slashes=False, ignore_url_check=True)
        
    # Simple Aliases For The Different Video Types
    def stream(self, resource: str, *args, **kwargs):
        # Check if stream location is a camera
        if resource.isnumeric():
            return self.stream_camera(int(resource), *args, **kwargs)
        # Else, assume its a file
        else:
            return self.stream_file(resource, *args, **kwargs)
    
    def stream_camera(self, camId: int, *args, name: str = "default", protocols: Optional[list[str]] = None, **kwargs):
        # Initialize Camera Video
        raise NotImplementedError()

    def stream_file(self, filename: str, *args, name: str = "default", protocols: Optional[list[str]] = None, **kwargs):
        # Initialize File Video
        from wormhole.video.filevideo import FileVideo
        video = FileVideo(filename, *args, **kwargs)
        self.add_managed_stream(video, name=name, protocols=protocols)
        
    def add_managed_stream(self, video: AbstractVideo, name: str = "default", protocols: Optional[list[str]] = None):
        # Check if advanced features are enabled
        if not self.advanced_features:
            raise Exception("Managed Streams Are Only Enabled If Advanced Features Are Enabled!")
        
        # Fill in list of protocols if not passed in
        protocols = protocols or list(self.supported_protocols.keys())
        if len(protocols) == 0:
            raise Exception("Protocols List Is Empty!")
        if any([p not in self.supported_protocols.keys() for p in protocols]):
            raise Exception("Protocols List Contains Unsupported Protocols!")
        
        # Process Name
        name = name.lower()
        if not name.isalnum():
            raise Exception("Name Must Be Alphanumeric!")
        if name in self.managed_streams:
            raise Exception(f"Name {name} Is Already Used!")
        
        # For each given protocol, start streaming!
        for proto in protocols:
            # Get the streamer class
            streamer, _ = self.supported_protocols[proto]
            # Initialize the streamer
            self.add_streamer(streamer, video, f"/wormhole/stream/{name}/{proto.lower()}", ignore_url_check=True)
            
        # Add the streamer to the list of managed streams
        self.managed_streams[name] = (video, protocols)
        return video
    
    def get_video(self, name: str = "default"):
        # Check if advanced features are enabled
        if not self.advanced_features:
            raise Exception("Managed Streams Are Only Enabled If Advanced Features Are Enabled!")
        
        if name not in self.managed_streams:
            raise Exception(f"Stream {name} Was Not Found!")
        
        return self.managed_streams[name][0]

    def view(self, name: str = "default", protocols: Optional[list[int]] = None):
        # Check if advanced features are enabled
        if not self.advanced_features:
            raise Exception("Managed Streams Are Only Enabled If Advanced Features Are Enabled!")
        
        raise NotImplementedError()
    
    def add_streamer(self, streamer: Type[AbstractStreamer], *args, **kwargs):
        # Initialize Streamer
        streamer_obj = streamer(self.controller, *args, **kwargs)
        # Add Streamer to Wormhole
        self.routes[streamer_obj.route] = streamer_obj
        
# Lightweight Wormhole Class for Just Reading Streams
class WormholeClient():
    pass
