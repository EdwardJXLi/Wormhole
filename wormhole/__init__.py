__version__ = "1.0.0"
from typing import Type
# from multiprocessing import Process
from threading import Thread

from wormhole.controller import AbstractController, FlaskController

# Entrypoint for everything WORMHOLE!
class Wormhole():
    def __init__(
        self, 
        # Basic Controller Settings
        network_controller: Type[AbstractController] = FlaskController,
        # Advanced Controller Settings
        # Extra Features
        welcome_screen: bool = True,
        # Pass All Other Arguments to the Controller
        *args,
        **kwargs
    ):
        # Create Controller
        self.controller = network_controller(*args, **kwargs)
        
        # Set up welcome screen
        if welcome_screen:
            def hello_world():
                return f"<h1>Welcome to Wormhole!</h1><p>Wormhole Video Streaming Server Running! Version: {__version__}</p>"
            self.controller.add_route("/", hello_world, strict_slashes=False)
            
        # Start Server In Another Thread
        self.wormhole_thread = Thread(target=self.controller.start_server)
        self.wormhole_thread.daemon = True
        self.wormhole_thread.start()
        
# Lightweight Wormhole Class for Just Reading Streams
class WormholeClient():
    pass
