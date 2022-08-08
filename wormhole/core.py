__version__ = "development"

# Setup Gevent Monkey Patching
try:
    from gevent import monkey
    monkey.patch_all()
except ModuleNotFoundError:
    print("Gevent is not installed. Ignoring Monkey Patch.")

import requests
import threading
from flask import request
from markupsafe import escape
from threading import Thread
from typing import Optional, Type

from wormhole.controller import AbstractController, FlaskController
from wormhole.streamer import AbstractStreamer
from wormhole.viewer import AbstractViewer
from wormhole.video import AbstractVideo


class Wormhole():
    """
    Entrypoint for everything WORMHOLE!
    """

    #
    # --- Basic Wormhole Setup ---
    #

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
        from wormhole.streamer import (
            RawJPEGStreamer,
            RawPNGStreamer,
            MJPEGStreamer
        )
        from wormhole.viewer import (
            RawJPEGViewer,
            RawPNGViewer,
            MJPEGViewer
        )
        self.supported_protocols = supported_protocols or {
            # ORDER MATTERS HERE! Ranked in order from most preferred to least preferred!
            "RAWJPEG": (RawJPEGStreamer, RawJPEGViewer),
            "RAWPNG": (RawPNGStreamer, RawPNGViewer),
            "MJPEG": (MJPEGStreamer, MJPEGViewer),
        }
        if self.advanced_features:
            if len(self.supported_protocols) == 0:
                raise Exception("No supported protocols were passed!")
            self.set_up_advanced_features()

        # Set up welcome screen
        if welcome_screen:
            def hello_world():
                return (
                    "<h1>Welcome to Wormhole!</h1>"
                    "<h3>If you see this page, Wormhole Video Streaming Server is successfully installed and working!</h3>"
                    f"<p>Version: {__version__}</p>"
                    f"{self.generate_debug_html() if self.controller.debug else ''}"  # type: ignore
                )
            self.controller.add_route("/", hello_world, strict_slashes=False)

        # Start Server In Another Thread
        self.wormhole_thread = Thread(target=self.controller.start_server, daemon=True)
        self.wormhole_thread.start()

    #
    # --- Advanced Wormhole Setup ---
    #

    def set_up_advanced_features(self):
        # Set up basic client sync
        def client_sync():
            # Default Response
            server_response = {
                "version": __version__,
                "supported_protocols": list(self.supported_protocols.keys()),
                "managed_streams": list(self.managed_streams.keys()),
            }

            # Get client information
            if not request.json:
                return {
                    "ready": False,
                    "message": "Invalid Client Information Sent!",
                    **server_response
                }, 400
            if not all(key in request.json for key in ["version", "supported_protocols"]):
                return {
                    "ready": False,
                    "message": "Posted Json Is Missing Fields!",
                    **server_response
                }, 400

            # Check if versions match
            client_version = request.json.get("version", "N/A")
            if client_version != __version__:
                return {
                    "ready": False,
                    "message": f"Wormhole Version Mismatch! Server: {__version__} Client: {client_version}",
                    **server_response
                }, 400

            # Get client supported protocols & verify if they are supported
            client_supported_protocols = request.json.get("supported_protocols", [])
            if not any([p in client_supported_protocols for p in self.supported_protocols.keys()]):
                return {
                    "ready": False,
                    "message": f"Client Does Not Support Any of The Supported Protocols! Server Supports: {list(self.supported_protocols.keys())} Client Supports: {client_supported_protocols}",
                    **server_response
                }, 400

            # Return with server information
            return {
                "ready": True,
                "message": f"Wormhole Is Ready To Connect!",
                **server_response
            }, 200

        self.controller.add_route("/wormhole/sync", client_sync, methods=["POST"], strict_slashes=False, strict_url=False)

        # Set Up Stream Sync
        def stream_sync(name):
            if name not in self.managed_streams:
                return "Stream Not Found!", 404

            # Get Stream Information
            video_obj, supported_protocols = self.managed_streams[name]

            # Return with server information
            server_response = {
                "version": __version__,
                "stream_name": name,
                "supported_protocols": supported_protocols,
                "stream_info": {
                    "width": video_obj.width,
                    "height": video_obj.height,
                    "pixel_size": video_obj.pixel_size,
                    "max_fps": video_obj.max_fps
                }
            }

            return server_response, 200
        self.controller.add_route("/wormhole/stream/<name>/sync", stream_sync, methods=["GET", "POST"], strict_slashes=False, strict_url=False)

    #
    # --- Managed Wormhole Streaming ---
    #

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

    def stream_file(
        self,
        filename: str,
        name: str = "default",
        protocols: Optional[list[str]] = None,
        video_fps: Optional[int] = None,
        stream_fps: Optional[int] = None,
        print_video_fps: bool = False,
        print_stream_fps: bool = False,
        **kwargs
    ):
        # Separate out kwargs for FileVideo object or Streamer Object
        # As FileVideo is constant, we can hardcode these.
        file_video_arg_keys = ["width", "height", "repeat", "cv2_config", "pixel_size", "frame_modifiers", "frame_subscribers"]
        file_video_args = {}
        streamer_args = {}
        for key, value in kwargs.items():
            if key in file_video_arg_keys:
                file_video_args[key] = value
            else:
                streamer_args[key] = value

        # Initialize File Video
        from wormhole.video import FileVideo
        video = FileVideo(filename, max_fps=video_fps, print_fps=print_video_fps, **file_video_args)

        self.stream_video(video, name=name, protocols=protocols, fps_override=stream_fps, print_fps=print_stream_fps, **streamer_args)

    def stream_video(self, video: AbstractVideo, *args, name: str = "default", protocols: Optional[list[str]] = None, **kwargs):
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
            self.create_stream(streamer, video, f"/wormhole/stream/{name}/{proto.lower()}", *args, strict_url=False, **kwargs)

        # Add the streamer to the list of managed streams
        self.managed_streams[name] = (video, protocols)
        return video

    #
    # --- Managed Wormhole Viewing ---
    #

    def view(self, hostname: str, name: str = "default"):
        # Check if advanced features are enabled
        if not self.advanced_features:
            raise Exception("Managed Streams Are Only Enabled If Advanced Features Are Enabled!")

        # Process Name
        name = name.lower()
        if not name.isalnum():
            raise Exception("Name Must Be Alphanumeric!")

        # Verify hostname is valid
        if not hostname.startswith("http://") and not hostname.startswith("https://"):
            hostname = f"http://{hostname}"
        if hostname.endswith("/"):
            hostname = hostname[:-1]
        # TODO: use regex to validate hostname, but idk regex

        # Sync with the server for information
        server_streams = self.sync_wormhole(hostname)
        if name not in server_streams:
            raise Exception(f"Requested Stream {name} not being streamed by the server! The current streams are: {server_streams}")

        # Sync Stream Information
        stream_protocols, stream_width, stream_height, stream_pixel_size, stream_fps = self.sync_stream(hostname, name)

        # Find best protocol to use for stream
        for proto in stream_protocols:
            if proto in self.supported_protocols.keys():
                best_protocol = proto
                break
        else:
            raise Exception(f"No Supported Protocols Found For Stream {name}! This error occurred after sync, which should never happen!")

        # Get the viewer class
        _, viewer = self.supported_protocols[best_protocol]

        # Initialize the viewer
        return viewer(f"{hostname}/wormhole/stream/{name}/{best_protocol.lower()}", stream_width, stream_height, max_fps=stream_fps, pixel_size=stream_pixel_size)

    def sync_wormhole(self, hostname: str):
        # Sync information with wormhole server
        resp = requests.post(
            url=f"{hostname}/wormhole/sync",
            json={
                "version": __version__,
                "supported_protocols": list(self.supported_protocols.keys())
            }
        )

        if resp.status_code != 200 and resp.status_code != 400:
            raise Exception(f"Failed To Sync With Wormhole Server! Error: [{resp.status_code}] {resp.text}")

        # Get the response
        resp_json = resp.json()
        if not resp_json:
            raise Exception("Failed To Sync With Wormhole Server! Invalid Json Response!")

        # Verify that all json fields are present
        # Yes, match exists, BUT this program is supposed to support python3.6 onwards
        if not all(key in resp_json for key in ["ready", "message", "version", "supported_protocols", "managed_streams"]):
            raise Exception("Failed To Sync With Wormhole Server! Missing Json Fields!")

        # Check if errored!
        if resp.status_code == 400:
            raise Exception(f"Failed To Sync With Wormhole Server! {resp_json.get('message', False)}")

        # NOTE: These should be checked by the server already, but just to double check, run again!
        # Check if server is ready
        if not resp_json.get("ready", False):
            raise Exception(f"Failed To Sync With Wormhole Server! Unknown Error: {resp_json}")

        # Check if version matches
        if resp_json.get("version", "N/A") != __version__:
            raise Exception(f"Failed To Sync With Wormhole Server! Version Mismatch! Server: {__version__} Client: {resp_json.get('version', 'N/A')}")

        # Check if server supports all protocols
        if not any([p in resp_json.get("supported_protocols", []) for p in self.supported_protocols.keys()]):
            raise Exception(f"Failed To Sync With Wormhole Server! Server Does Not Have Any Supported Protocols!")

        # Return with server information
        return resp_json.get("managed_streams", [])

    def sync_stream(self, hostname: str, name: str):
        # Sync information with wormhole server
        resp = requests.get(
            url=f"{hostname}/wormhole/stream/{name}/sync"
        )

        if resp.status_code != 200:
            raise Exception(f"Failed To Sync With Wormhole Stream! Error: [{resp.status_code}] {resp.text}")

        # Get the response
        resp_json = resp.json()
        if not resp_json:
            raise Exception("Failed To Sync With Wormhole Stream! Invalid Json Response!")

        # Verify that all json fields are present
        # Yes, match exists, BUT this program is supposed to support python3.6 onwards
        if not all(key in resp_json for key in ["version", "stream_name", "supported_protocols", "stream_info"]):
            raise Exception("Failed To Sync With Wormhole Stream! Missing Json Fields!")

        # Verify Stream Response
        stream_info = resp_json.get("stream_info")
        if not all(key in stream_info for key in ["width", "height", "pixel_size", "max_fps"]):
            raise Exception("Failed To Sync With Wormhole Stream! Stream Info is Missing Json Fields!")

        return resp_json.get("supported_protocols"), stream_info.get("width", 0), stream_info.get("height", 0), stream_info.get("pixel_size", 0), stream_info.get("max_fps", 0)

    #
    # --- Helper Streaming Functions ---
    #

    def create_stream(self, streamer: Type[AbstractStreamer], *args, **kwargs):
        # Initialize Streamer
        streamer_obj = streamer(self.controller, *args, **kwargs)
        # Add Streamer to Wormhole
        self.routes[streamer_obj.route] = streamer_obj

    def get_video(self, name: str = "default"):
        # Check if advanced features are enabled
        if not self.advanced_features:
            raise Exception("Managed Streams Are Only Enabled If Advanced Features Are Enabled!")

        name = name.lower()
        if name not in self.managed_streams:
            raise Exception(f"Stream {name} Was Not Found!")

        return self.managed_streams[name][0]

    def join(self):
        # Joins the wormhole thread so that the app does not exit
        self.wormhole_thread.join()

    def generate_debug_html(self):
        output = ""
        output += "<h2>Debug Information</h2>"
        output += f"<h3>Advanced Features Enabled: {self.advanced_features}</h3>"
        output += f"<h3>Supported Protocols:</h3>"
        for proto, (streamer, viewer) in self.supported_protocols.items():
            output += f"<p>[{proto}] Streamer: {escape(streamer)} | Viewer: {escape(viewer)}<p>"
        output += f"<h3>Enabled Routes:</h3>"
        for route, streamer in self.routes.items():
            output += f"<p>{route} | Streamer: {escape(streamer)}</p>"
        output += f"<h3>Managed Streams:</h3>"
        for name, (video, protocols) in self.managed_streams.items():
            output += f"<p>{name} | Video Object: {escape(video)} | Supported Protocols: {protocols}</p>"
        output += f"<h3>Tunning Threads:</h3>"
        for thread_id, thread in enumerate(threading.enumerate()):
            output += f"<p>{thread_id} | {escape(thread)}</p>"
        return output


class WormholeClient():
    """
    TODO: Lightweight Wormhole Class for Just Reading Streams
    """
    pass
