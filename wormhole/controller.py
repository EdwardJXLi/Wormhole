from typing import Callable, Any

from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from typing import Optional
import uuid

class AbstractController():
    def __init__(self, *args, **kwargs):
        raise NotImplementedError()
    
    def get_app(self):
        raise NotImplementedError()
    
    def add_route(self, route: str, handler: Callable, *args, **kwargs):
        raise NotImplementedError()
    
    def add_message_handler(self, message: str, handler: Callable, *args, **kwargs):
        raise NotImplementedError()
    
    def start_server(self, *args, **kwargs):
        raise NotImplementedError()
    
    def stop_server(self, *args, **kwargs):
        raise NotImplementedError()

class FlaskController(AbstractController):
    def __init__(
        self, 
        wormhole,
        cors: bool = True, 
        host: str = "0.0.0.0", 
        port: int = 8000,
        flask_config: dict[str, Any] = {},
        debug: bool = False,
        *args,
        **kwargs
    ):
        # Create The Flask Server
        self.wormhole = wormhole
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.debug = debug
        self.server_args = args
        self.server_kwargs = kwargs
        
        # Set Flask Config Vars
        for k, v in flask_config.items():
            self.app.config[k] = v
            
        # Setup socketio
        self.socketio = SocketIO(self.app, logger=self.debug, engineio_logger=self.debug, cors_allowed_origins="*")
            
        # Enable CORS on the server
        if cors:
            CORS(self.app)
            
        # Set logging if debug
        if self.debug:
            import logging
            logging.basicConfig(level=logging.DEBUG)
            
        # Monkey Patch _is_setup_finished so that dynamic route additions are allowed
        self.app._is_setup_finished = lambda: False
        
    def get_app(self):
        return self.app
            
    def add_route(self, route: str, handler: Callable, *args, strict_url: bool = True, **kwargs):
        # Validate Route
        if not route.startswith('/'):
            raise ValueError("Route must start with '/'")
        if route in self.wormhole.routes:
            raise ValueError(f"Route {route} already exists")
        if self.wormhole.advanced_features and strict_url and route.startswith('/wormhole'):
            print("Warning: the 'wormhole' keyword in the route is reserved. Using it may cause issues.")
            
        # Hot-add handler for route
        self.app.add_url_rule(route, endpoint=str(uuid.uuid4()), view_func=handler, *args, **kwargs)
    
    def add_message_handler(self, message: str, handler: Callable, namespace: Optional[str] = None, *args, strict_url: bool = True, **kwargs):
        # Validate Namespace
        if namespace:
            if not namespace.startswith('/'):
                raise ValueError("Route must start with '/'")
            if namespace in self.wormhole.routes:
                raise ValueError(f"Namespace {namespace} already exists")
            if self.wormhole.advanced_features and strict_url and namespace.startswith('/wormhole'):
                print("Warning: the 'wormhole' keyword in the namespace is reserved. Using it may cause issues.")
            
        # Hot-add handler for socketio message
        self.socketio.on(message, namespace=namespace, *args, **kwargs)(handler)
        # Warning: a little cursed :/
        
    def start_server(self, *args, **kwargs):
        # self.app.run(host=self.host, port=self.port, *args, **kwargs)
        self.socketio.run(
            self.app, 
            log_output=self.debug, 
            host=self.host, 
            port=self.port, 
            debug=self.debug, 
            use_reloader=False, 
            *[*args, *self.server_args],  # Merge *args and *self.server_args
            **{**kwargs, **self.server_kwargs}  # Merge **kwargs and **self.server_kwargs
        )
