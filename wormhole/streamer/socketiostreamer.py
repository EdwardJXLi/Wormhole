from wormhole.streamer import AbstractStreamer

from flask_socketio import join_room
from threading import Thread
from typing import Callable

# Base Class for Everything SocketIO Streamer
class SocketIOStreamerBase(AbstractStreamer):
    def __init__(
        self, 
        video_streamer: Callable,
        *args, 
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        # Main hotloop to run for video streams
        self.video_streamer = video_streamer
        
        # Control variables to save on execution when no clients are connected
        self.thread_running = False
        self.connected_clients = 0

        # Setup Background Video Thread
        self.video_streamer_thread = Thread(target=self.video_streamer)
                
        # Add Connect Handler
        def on_connect():
            self.connected_clients += 1
            # Start the video streamer if it is not already running
            if self.thread_running == False:
                self.thread_running = True
                self.video_streamer_thread = Thread(target=self.video_streamer)
                self.video_streamer_thread.start()
            
            # Tell client to join the video room
            join_room("video_feed")
        self.controller.add_message_handler("connect", on_connect, namespace=self.route, strict_url=self.strict_url)
        
        # Add Disconnect Handler
        def on_disconnect():
            self.connected_clients -= 1
            
            # If no clients are connected anymore, stop server
            if self.connected_clients == 0:
                self.thread_running = False
        self.controller.add_message_handler("disconnect", on_disconnect, namespace=self.route, strict_url=self.strict_url)
