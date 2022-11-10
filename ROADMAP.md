# Wormhole Roadmap
Wormhole was originally a simple weekend project to consolidate everything I needed in real-time video streaming into one simple-to-use library. As the project grew, I saw how much potential it had to do much more as an all-in-one video, camera, and data streaming library for Python. That is why I divided Wormhole's development into five generations. 

- Generation One is all the essential features I need for a usable streaming library. This includes basic mjpeg and raw streams, but also basic protocol negotiations and a simple-to-use API. 
- Generation Two expands on gen one to make Wormhole a fully-fledged streaming library with all the convenience features I could need.
- Generation Three expands on gen two to support high bitrate streams, hopefully bringing real-time 4k60fps streams over the air. 
- Finally, Generation Four and beyond are all the visions I have to make Wormhole a fully-fledged video streaming library capable of emulating other tools like Zoom or Google Meet.

Of course, this project won't be done in just over a weekend or two. Wormhole's development will most likely last for years, adding incremental features whenever I feel it's missing. If you would like to help with this journey, feel free to submit a PR anytime. Nevertheless, the goals shown below are just preliminary plans, so if you feel like there is a feature that is missing, feel free to edit this list!

## ~~ Generation 1 ~~ DONE!
- [X] Initial Setup
    - [X] Flask Server Setup
        - [X] Dynamic Flask Routes
    - [X] SocketIO Server Setup
        - [X] Dynamic SocketIO Handlers
        - [X] Dynamic SocketIO Rooms
    - [X] Proper Framerate Control
- [X] Basic Video Rendering Functionality
    - [X] Webcam / Cameras
    - [X] Video Files
    - [X] Image Files
    - [X] Copies of Videos
    - [X] Custom Video Streams
- [X] Basic Video Streaming Functionality
    - [X] MJPEG Streams
    - [X] Raw Image Streams
    - [X] Raw Streams
- [X] Basic Video Viewing Functionality
    - [X] MJPEG Streams
    - [X] Raw Image Streams
    - [X] Raw Streams
- [X] Managed Streaming
    - [X] Syncing
      - [X] Client-Server Sync
      - [X] Stream Information Sync
      - [X] Stream Synchronization
      - [X] Basic Protocol Negotiation
- [X] Basic Video Processing
    - [X] Dynamic Video Manipulation
    - [X] Video Modifiers
    - [X] Video Subscribers
- [X] Error Handling
    - [X] Rendered Error Messages
    - [X] Logging
- [X] Writing Video to File
    - [X] Multi Codec Support
    - [X] .MP4 Support
    - [X] .AVI Support
    - [X] .WEBM Support
    - [X] Threaded Support
- [X] Example Code

## Generation 2
- [ ] Using a Python profiler to iron out performance issues
- [ ] Publish on PyPi
- [ ] Lightweight Javascript Client
- [ ] Lightweight Python Client
- [X] SSL support
- [ ] Dynamic FPS
    - [X] Server Support
    - [ ] Client Support
- [ ] Advanced Protocol Negotiation
    - [ ] Dynamic Python Module Loading instead of static
    - [ ] Dynamic Negotiation Depending On What Modules Are Loaded
    - [X] Use Fallback is one fails
    - [ ] Multiple Attempts in case of network failure
- [ ] Advanced Video Rendering Functionality
    - [ ] Render Video from Streaming Sites
        - [ ] Youtube
        - [ ] Vimeo
        - [ ] Twitch
- [ ] Advanced Video Streaming Functionality
    - [X] b64 Streams
    - [ ] TurboJpeg Streams
- [ ] Advanced Video Viewing Functionality
    - [X] b64 Streams
    - [ ] TurboJpeg Streams
- [X] Advanced Video Processing
    - [X] Text Rendering
        - [X] FPS Rendering
        - [X] Debug Rendering
    - [X] Image Rendering
        - [X] Transparency Rendering
        - [X] Wormhole Watermark
- [ ] Advanced Video File Writing
    - [ ] Chunking (new file every x minutes)
    - [ ] Autodetect Video Capabilities
    - [ ] Controllable Video Thread
- [ ] Interactive Shell Fix / Support

## Generation 3
- [ ] Ability to start and stop streams
    - [ ] Ability to pause and resume streams
    - [ ] Safe thread closures
- [ ] Syncing Color Space
    - [X] Syncing Pixel Size
    - [ ] Automatic Color Space Conversion
- [ ] Dynamic Protocol Switching
    - [ ] Server
    - [ ] Client
- [ ] ZMQ Compatibility
    - [ ] Server
    - [ ] Client
    - [ ] Integration
- [ ] WebRTC Compatibility
    - [ ] Server
    - [ ] Client
- [ ] 4k 60fps Streaming Capability

## Generation 4
- [ ] Dynamic resizing of video frames
- [ ] Dynamic Bitrate Control
- [ ] 🔊 Sound Sharing!!!
- [ ] File Sharing
- [ ] HLS Support
    - [ ] Server
    - [ ] Client
- [ ] RTMP Support
    - [ ] Server
    - [ ] Client
- [ ] MPEG-DASH Support
    - [ ] Server
    - [ ] Client
- [ ] More advanced authentication & permission management

## Generation 5
- [ ] More Clients on More Platforms
    - [ ] Javascript/Typescript Client & Server
    - [ ] Java/Kotlin Client & Server
    - [ ] C/C++ Client & Server
- [ ] Realtime streaming to Twitch, Youtube, & More
- [ ] VR video
- [ ] Surround Sound

## Generation 6
- [ ] Emulating the entire universe!
