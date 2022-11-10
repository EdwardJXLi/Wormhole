#
# == Wormhole Example Viewer ==
# 
# This example shows how to use Wormhole to view and render a screen onto a window. 
#

from wormhole import Wormhole
from wormhole.video import render_video

# Create Wormhole Object. Port is set to 8001 to not conflict with other running server
wormhole = Wormhole(port=8001)

# Connect to server
video = wormhole.view("http://localhost:8000")

# Render the video onto a window
render_video(video)
