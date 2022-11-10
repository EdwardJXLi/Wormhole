#
# == Wormhole Example Stream ==
# 
# This example shows how to use the Wormhole library to stream a webcam.
#

from wormhole import Wormhole

# Create Wormhole Object
wormhole = Wormhole()

# Tell wormhole to stream this file
wormhole.stream_camera(0)

# Keep the server alive
wormhole.join()

# Thats It!
# Now go to http://localhost:8000/wormhole/stream/default/mjpeg to view the video!
