from wormhole.utils import FrameController
from wormhole.streamer import AbstractStreamer

import time
from flask_socketio import emit, join_room
from threading import Thread
from typing import Any, Callable


class SocketIOStreamerBase(AbstractStreamer):
    """
    Base Class for Everything SocketIO Streamer
    """

    def __init__(
        self,
        frame_publisher_hotloop: Callable,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        # Main loop to run for video streams
        self.frame_publisher_hotloop = frame_publisher_hotloop

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

    # Streamer simple  for raw video
    def video_streamer(self):
        # Get the flask context
        with self.controller.get_app().app_context():
            frame_controller = FrameController(self.max_fps, print_fps=self.print_fps)
            while True:
                if not self.thread_running:
                    return  # Kill the thread if no clients are connected

                # Run Stream Publisher Function
                # This should process any video encoding work and publishing logic
                self.frame_publisher_hotloop()

                frame_controller.next_frame()

    # Helper function to emit socket information
    def send_data(self, data: Any):
        emit("frame", data, room="video_feed", namespace=self.route, broadcast=True)

        time.sleep(0)  # Force A Network Buffer Flush
        # Technically this should be a gevent.sleep(0) but time.sleep is monkey patched so this should be alright.

        return True
