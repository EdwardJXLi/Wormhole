# Wormhole: Realtime Streaming Engine
Wormhole is a Simple and Hackable Realtime Video Streaming Engine for Prototypes and Projects alike!

## Features:
- Multithreaded Flask & SocketIO Backend
- Camera and Video File Streaming!
- Fast and scalable Motion JPEG and PNG streaming
- Dynamic protocol negotiation between Wormhole servers and clients
- Dynamic video modification through callbacks and views

## What is Wormhole?
Wormhole is not meant to overtake established battle-tested libraries such as WebRTC or alike. Instead, Wholehole aims to be an extremely simple-to-use library wherever you need to share video (Pre-recorded or live from a camera) between two or more servers. The original design goal was so that Wormhole could be utilized during fast-paced development environments such as hackathons and other competitions, Yet flexible and modular enough to be a one-stop-shop for your next AI video processing project, webcam streaming project, or simple video sharing project.

## Installing Wormhole
To get started with Wormhole, you can just clone the project by running `git clone git@github.com:RadioactiveHydra/Wormhole.git` to your local machine.
Once downloaded, run `pip install -r wormhole/requirements.txt` to install all the required dependencies.
> NOTE: It is recommended that you install Wormhole in a virtual env! More instructions can be found [here](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)

## Getting Started with Wormhole
> NOTE: This is still WIP! API may change and/or be removed in future releases.  

To start streaming from your camera, all you need to write is:
```py
from wormhole import Wormhole
server = Wormhole()
server.stream(0)
server.join()
```

**Thats It!** Wormhole then handles setting up the server, launching the camera, and streaming the video frames!
To stream from a video file instead, you can write the following:
```py
from wormhole import Wormhole
server = Wormhole()
server.stream("path/to/video.mp4")
server.join()
```

As easy as that! To view the video stream in another python project, you can just run:
```py
from wormhole import Wormhole
video = Wormhole().view("your.ip.address.here")
```

Again, **thats it!** Wormhole then handles setting up the client, negotiating the best streaming protocol to use, and viewing the video stream! To render the video to your screen, you can then run:
```py
from wormhole.utils import render_video
render_video(video)
```
The video stream is also available online if you go to `http://localhost:5000/wormhole/stream/default/mjpeg` in your browser.

Of course, you may want to do more than what Wormhole offers by default. For that, you can read up on the Advanced Usage Guide. (WIP)

## Why develop Wormhole?
After rewriting the same video streaming codebase for the 5th hackathon/project in a row, I thought it was time to sit down and write a universal streaming library for all my needs. Shopping around online did not yield any projects that fit my needs, so I decided to build my own. Wormhole is designed so that it can not only be deployed in ~~minutes~~ **seconds**, but it is also flexible enough to do everything I need in a fully-fledged data streaming library.

## Contributing to Wormhole
Wormhole's source code follows all **PEP8** guidelines (except E501 for long lines). Also, most function arguments are **typed** so that the API is coherent and easy-to-use. Finally, Wormhole aims to keep compatibility for **Python versions 3.6 and beyond**. To contribute to Wormhole, you can either fork the project on GitHub or submit a pull request. If you have any questions or suggestions, feel free to join the discord server here: [https://discord.gg/9QF2bPc](https://discord.gg/9QF2bPc).
