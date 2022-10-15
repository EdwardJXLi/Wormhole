import logging
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from typing import Any, Callable, Optional
from uuid import uuid4


class AbstractController():
    """
    Base Class for All Network Controllers
    """

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
    """
    Flask Network Controller with a SocketIO Backend
    """

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
        # Check if script is being run from an interactive shell
        # If it is, return warning / error message
        import __main__ as main
        if not hasattr(main, '__file__'):
            logging.warning("Wormhole does not work in an interactive shell!")
            logging.warning("Please run your script from a file.")
            logging.warning("This is a known issue that is WIP.")
            
        # Create The Flask Server
        self.wormhole = wormhole
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.debug = debug
        self.server_args = args
        self.server_kwargs = kwargs
        logging.debug(f"Initializing Flask Server on {host}:{port}")
        logging.debug(f"Flask Arguments: {args}, {kwargs}")

        # Set Flask Config Vars
        for k, v in flask_config.items():
            self.app.config[k] = v

        # Setup socketio
        self.socketio = SocketIO(self.app, logger=self.debug, engineio_logger=self.debug, cors_allowed_origins="*")

        # Enable CORS on the server
        if cors:
            CORS(self.app)

        # Monkey Patch _is_setup_finished so that dynamic route additions are allowed
        self.app._is_setup_finished = lambda: False  # type: ignore

    def get_app(self):
        return self.app

    def add_route(self, route: str, handler: Callable, *args, strict_url: bool = True, **kwargs):
        logging.debug(f"Adding Route {route} with handler {handler}")
        # Validate Route
        if not route.startswith('/'):
            raise ValueError("Route must start with '/'")
        if route in self.wormhole.routes:
            raise ValueError(f"Route {route} already exists")
        if self.wormhole.advanced_features and strict_url and route.startswith('/wormhole'):
            logging.warning("The 'wormhole' keyword in the route is reserved. Using it may cause issues.")

        # Hot-add handler for route
        self.app.add_url_rule(route, endpoint=str(uuid4()), view_func=handler, *args, **kwargs)

    def add_message_handler(self, message: str, handler: Callable, namespace: Optional[str] = None, *args, strict_url: bool = True, **kwargs):
        logging.debug(f"Adding SocketIO Message Handler for Message {message} on namespace {namespace} with handler {handler}")
        # Validate Namespace
        if namespace:
            if not namespace.startswith('/'):
                raise ValueError("Route must start with '/'")
            if namespace in self.wormhole.routes:
                raise ValueError(f"Namespace {namespace} already exists")
            if self.wormhole.advanced_features and strict_url and namespace.startswith('/wormhole'):
                logging.warning("The 'wormhole' keyword in the namespace is reserved. Using it may cause issues.")

        # Hot-add handler for socketio message
        self.socketio.on(message, namespace=namespace, *args, **kwargs)(handler)
        # Warning: a little cursed :/

    def start_server(self, *args, **kwargs):
        logging.info(f"Starting Flask Server on {self.host}:{self.port}")
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
