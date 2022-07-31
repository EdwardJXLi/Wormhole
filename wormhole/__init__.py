__version__ = "1.0.0"
from typing import Type, Union
from multiprocessing import Process

from wormhole.controller import AbstractController, FlaskController

# Entrypoint for everything WORMHOLE!
class Wormhole():
    def __init__(
        self, 
        # Basic Controller Settings
        network_controller: Type[AbstractController] = FlaskController,
        cors: bool = True,
        host: str = "0.0.0.0",
        port: Union[int, str] = 8000,
        # Advanced Controller Settings
        # Extra Features
        welcome_screen: bool = True
    ):
        # Create Controller
        self.controller = network_controller(cors=bool(cors), host=host, port=int(port))
        
        # Set up welcome screen
        if welcome_screen:
            def hello_world():
                return f"<h1>Welcome to Wormhole!</h1><p>Wormhole Video Streaming Server Running! Version: {__version__}</p>"
            self.controller.add_route("/", hello_world, strict_slashes=False)
            
        # Start Server In Another Process
        self.wormhole_process = Process(target=self.controller.start_server)
        self.wormhole_process.start()
        
# Lightweight Wormhole Class for Just Reading Streams
class WormholeClient():
    pass
