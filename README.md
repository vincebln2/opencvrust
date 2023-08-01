# opencvrust
This repository contains the opencv code I worked on in the summer of 2023. We have opencv code in Python, and I rewrote those in Rust for fun and to see if there was any performance benefit (spoiler alert: benefit was negligible, but Rust is fun to work in so it's ok).

*The lack of benefit in question refers to the amount of time it took to send an image captured in the camera to a webpage ran on a local server, so it makes sense that there was no decrease in the amount of time the process took as the time delay was primarily network related.

Camera used: Arducam 16MP Autofocus USB Camera for Computer with Microphone - X002RJB3KT
## live_view_rust
Configures camera then opens a GUI window that shows a live video feed of a usb camera, quit out of the window by pressing 'q'

## video_view_rust 
Configures camera focus, white balance, exposure, and autofocus. Also configures video resolution, frame rate, encoder type, length, and filename, then records a video according to those settings. The time length of the video is dependent on the fps selected (30 in this case) and the number of frames to be captured, 150 in this case, meaning the video will be 5 seconds long @30fps.

## video-view and live-view
Contains Python equivalents to the rust code here.

## Issues
The camera_config() functions are not reliable. This issue lies in the firmware of the cameras we used, for some reason it does not listen to v4l2-ctl commands for manually adjusting white balance, focus, and exposure. 

Captured video and frames look "fine" when white balance, focus, and exposure are all set to automatic, but we do not want these values to be automatic on the Tapster 3 robots. For example, we want focus to stay at one value so the camera can stay focused on the touch screen and not change when the robot's end effector moves in front of it.

The problem occurs when there is an attempt to manually set white balance, focus, and exposure values. When v4l2-ctl commands are sent to turn off automatic settings, and one tries to set the values manually, they often do not change from the original value or do not change to the desired value. We found that capturing a few frames before and after attempting to configure before actually trying to use the frames makes camera configuration work more consistently, but still not 100% of the time.

