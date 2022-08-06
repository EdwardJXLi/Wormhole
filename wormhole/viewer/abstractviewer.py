from wormhole.video import AbstractVideo


class AbstractViewer(AbstractVideo):
    """
    General Abstract Viewer Class for Wormhole. 
    """

    def __init__(
        self,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
