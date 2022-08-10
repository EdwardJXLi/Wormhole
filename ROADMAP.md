# Wormhole Roadmap
Wormhole was originally a simple weekend project to consolidate everything I needed in real-time video streaming into one simple-to-use library. As the project grew, I saw how much potential it had to do much more as an all-in-one video, camera, and data streaming library for Python. That is why I divided Wormhole's development into five generations. 

- Generation One is all the essential features I need for a usable streaming library. This includes basic mjpeg and raw streams, but also basic protocol negotiations and a simple-to-use API. 
- Generation Two expands on gen one to make Wormhole a fully-fledged streaming library with all the convenience features I could need.
- Generation Three expands on gen two to support high bitrate streams, hopefully bringing real-time 4k60fps streams over the air. 
- Finally, Generation Four and beyond are all the visions I have to make Wormhole a fully-fledged video streaming library capable of emulating other tools like Zoom or Google Meet.

Of course, this project won't be done in just over a weekend or two. Wormhole's development will most likely last for years, adding incremental features whenever I feel it's missing. If you would like to help with this journey, feel free to submit a PR anytime. Nevertheless, the goals shown below are just preliminary plans, so if you feel like there is a feature that is missing, feel free to edit this list!

## Generation 1
- [X] Initial Setup
    - [X] Flask Server Setup
        - [X] Dynamic Flask Routes
    - [X] SocketIO Server Setup
        - [X] Dynamic SocketIO Handlers
        - [X] Dynamic SocketIO Rooms
    - [X] Proper Framerate Control
- [ ] Basic Video Rendering Functionality
    - [ ] Webcam / Cameras
    - [X] Video Files
    - [ ] Image Files
    - [X] Copies of Videos
    - [ ] Custom Video Streams
- [ ] Basic Video Streaming Functionality
    - [X] MJPEG Streams
    - [X] Raw Image Streams
    - [X] Raw Streams
- [ ] Basic Video Viewing Functionality
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
- [ ] Error Handling
    - [ ] Rendered Error Messages
    - [ ] Logging
- [ ] Example Code

## Generation 2
- [ ] Using a Python profiler to iron out performance issues
- [ ] Publish on PyPi
- [ ] Lightweight Javascript Client
- [ ] Lightweight Python Client
- [X] SSL support
- [ ] Dynamic FPS
    - [X] Server Support
    - [ ] Client Support
- [ ] Dynamic Python Module Loading instead of static
- [ ] Sophisticated Video Streaming Functionality
    - [X] b64 Streams
    - [ ] TurboJpeg Streams
- [ ] Sophisticated Video Viewing Functionality
    - [X] b64 Streams
    - [ ] TurboJpeg Streams
- [X] Sophisticated Video Processing
    - [X] Text Rendering
        - [X] FPS Rendering
        - [X] Debug Rendering
    - [X] Image Rendering
        - [X] Transparency Rendering
        - [X] Wormhole Watermark

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