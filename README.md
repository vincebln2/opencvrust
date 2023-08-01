# opencvrust
This repository contains the opencv code I worked on in the summer of 2023. About half of it is in rust, and the other half in python. The python code was what we originally had, and I wanted to replicate that code in rust for fun/to see if there were any performance benefits for our applications.

Camera used: Arducam 16mp autofocus usb camera
## live_view_rust
Configures camera then opens a GUI window that shows a live video feed of a usb camera, quit out of window by pressing 'q'

## video_view_rust 
Configures camera focus, white balance, exposure, and autofocus. Also configures video resolution, frame rate, encoder type, length, and filename, then records a video according to those settings. Time length of video dependent on fps selected (30 in this case) and the number of frames to be captured, 150 in this case, meaning the the video will be 5 seconds long @30fps.

## Issues
The camera_config() functions are not reliable. This issue lies in the firmware of the cameras we used, for some reason it does not listen to v4l2-ctl commands for manually adjusting white balance, focus, and exposure. 

Captured video and frames look "fine" when white balance, focus, and exposure are all set to automatic, but we do not want these values to be automatic on the tapster 3 robots. For example, we want focus to stay at one value so the camera can stay focused on the touch screen and not change when the end effector of the robot moves in front of it.

The problem occurs when there is an attempt to manually set white balance, focus, and exposure values. When v4l2-ctl commands are sent to turn off automatic settings, and one tries to manually set the values, they often do not change from the original value or do not change to the desired value. We found that capturing a few frames before and after attempting to configure before actually trying to use the frames makes camera configuration work more consistently, but still not 100% of the time.

