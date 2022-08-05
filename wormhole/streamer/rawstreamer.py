from wormhole.streamer.socketiostreamer import SocketIOStreamerBase

# Raw Image Streaming
# This is generally not recommended as it sends A LOT of information over the network, 
# But its an interesting experiment to see the maximum processing throughput
# Without any image encoding
class RawStreamer(SocketIOStreamerBase):
    def __init__(
        self, 
        *args,
        **kwargs
    ):
        # Initiate Parent SocketIO Streamer Object
        super().__init__(self.stream_hotloop, *args, **kwargs)
    
    # Hotloop for sending raw video
    def stream_hotloop(self):
        self.send_data(self.video.get_frame().tobytes())
