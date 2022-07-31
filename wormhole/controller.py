from flask import Flask
from flask_cors import CORS

class AbstractController():
    def __init__(self, *args, **kwargs):
        raise NotImplementedError()
    
    def add_route(self, route, func, *args, **kwargs):
        raise NotImplementedError()
    
    def start_server(self, *args, **kwargs):
        raise NotImplementedError()
    
    def stop_server(self, *args, **kwargs):
        raise NotImplementedError()

class FlaskController(AbstractController):
    def __init__(self, cors=True, host="0.0.0.0", port=8000):
        # Create The Flask Server
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        # Enable CORS on the server
        if cors:
            CORS(self.app)
            
    def add_route(self, route, func, *args, **kwargs):
        self.app.add_url_rule(route, view_func=func, *args, **kwargs)
        
    def start_server(self, *args, **kwargs):
        self.app.run(host=self.host, port=self.port, *args, **kwargs)
