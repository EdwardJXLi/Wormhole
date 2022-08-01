from wormhole.video import AbstractVideo

# General Abstract Viewer Class for Wormhole. 
class AbstractViewer(AbstractVideo):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
