from typing import Callable, Any
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

class AbstractController():
    def __init__(self, *args, **kwargs):
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
        cors: bool = True, 
        host: str = "0.0.0.0", 
        port: int = 8000,
        flask_config: dict[str, Any] = {},
        debug: bool = False
    ):
        # Create The Flask Server
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.debug = debug
        
        # Set Flask Config Vars
        for k, v in flask_config.items():
            self.app.config[k] = v
            
        # Setup socketio
        self.socketio = SocketIO(self.app, logger=self.debug, engineio_logger=self.debug, cors_allowed_origins="*")
            
        # Enable CORS on the server
        if cors:
            CORS(self.app)
            
    def add_route(self, route: str, handler: Callable, *args, **kwargs):
        # Hot-add handler for route
        self.app.add_url_rule(route, view_func=handler, *args, **kwargs)
    
    def add_message_handler(self, message: str, handler: Callable, *args, **kwargs):
        # Hot-add handler for socketio message
        self.socketio.on(message, *args, **kwargs)(handler)
        # Warning: a little cursed :/
        
    def start_server(self, *args, **kwargs):
        # self.app.run(host=self.host, port=self.port, *args, **kwargs)
        self.socketio.run(self.app, host=self.host, port=self.port, debug=self.debug, use_reloader=False, *args, **kwargs)
