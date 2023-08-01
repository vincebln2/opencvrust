import os
import sys
import cv2
import time

# Set image resolution
#frame_width = 4656  # 10fps
#frame_height = 3496
frame_width = 3840  # 10fps
frame_height = 2160
#frame_width = 2592  # 10fps
#frame_height = 1944
#frame_width = 2320  # 30fps
#frame_height = 1744

# Set Frame Per Second rate
fps = 5

def camera_config():
    print("Camera config: Starting") 

    os.system("v4l2-ctl --device /dev/video0 --set-ctrl=focus_automatic_continuous=1")
    time.sleep(2)

    # Focus
    os.system("v4l2-ctl --device /dev/video0 --set-ctrl=focus_automatic_continuous=0")    
    os.system("v4l2-ctl --device /dev/video0 --set-ctrl=focus_automatic_continuous=1")
    os.system("v4l2-ctl --device /dev/video0 --set-ctrl=focus_automatic_continuous=0")    
    os.system("v4l2-ctl --device /dev/video0 --set-ctrl=focus_absolute=432")
    os.system("v4l2-ctl --device /dev/video0 --set-ctrl=focus_absolute=1") 
    os.system("v4l2-ctl --device /dev/video0 --set-ctrl=focus_absolute=432")       
    time.sleep(1) 

    # Exposure
    # The 'ol turn it off and turn it back on trick...
    os.system("v4l2-ctl --device /dev/video0 --set-ctrl=auto_exposure=1")
    os.system("v4l2-ctl --device /dev/video0 --set-ctrl=auto_exposure=3")
    os.system("v4l2-ctl --device /dev/video0 --set-ctrl=auto_exposure=1")
    os.system("v4l2-ctl --device /dev/video0 --set-ctrl=exposure_time_absolute=1500")
    os.system("v4l2-ctl --device /dev/video0 --set-ctrl=exposure_time_absolute=1") 
    os.system("v4l2-ctl --device /dev/video0 --set-ctrl=exposure_time_absolute=1500")       
    time.sleep(1) 

    # White Balance
    # The 'ol turn it off and turn it back on trick...
    os.system("v4l2-ctl --device /dev/video0 --set-ctrl=white_balance_automatic=0")
    os.system("v4l2-ctl --device /dev/video0 --set-ctrl=white_balance_automatic=1")
    time.sleep(5)
    os.system("v4l2-ctl --device /dev/video0 --set-ctrl=white_balance_automatic=0")
    #os.system("v4l2-ctl --device /dev/video0 --set-ctrl=white_balance_temperature=3540")
    #os.system("v4l2-ctl --device /dev/video0 --set-ctrl=white_balance_temperature=2800")  
    #os.system("v4l2-ctl --device /dev/video0 --set-ctrl=white_balance_temperature=3540")      
    #os.system("v4l2-ctl --device /dev/video0 --set-ctrl=white_balance_temperature=4600")    
    #os.system("v4l2-ctl --device /dev/video0 --set-ctrl=white_balance_temperature=4000")    
    os.system("v4l2-ctl --device /dev/video0 --set-ctrl=white_balance_temperature=4600")    
    time.sleep(2)

    print("Camera config: Complete")


if __name__ == '__main__':
  # Open connection to camera
  cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
  cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

  # Get the settings (to make sure they were set correctly)
  prop_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  prop_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  cc = int(cap.get(cv2.CAP_PROP_FOURCC))
  fourcc = chr(cc & 0xff) + chr((cc >> 8) & 0xff) + chr((cc >> 16) & 0xff) + chr((cc >> 24) & 0xff)
  print('Video settings: ' + str(prop_width) + 'x' + str(prop_height) + ' / ' + fourcc)

  # Read one frame.
  # Apparently camera settings get reset by the first cap.read(),
  # ... so we need to read a frame before we change any other camera settings
  #grabbed, frame = cap.read()

  # Read frames and write the last one to file.
  # This flushes out the initial frames from the camera's buffer that
  # might be out of focus.
  for i in range(20):
    ret, frame = cap.read()

  # Set camera configuration
  camera_config()
  
  for i in range(20):
    ret, frame = cap.read()

  cv2.imwrite("frame.jpg", frame)
  
  out = cv2.VideoWriter('video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height), True)

  # Finally, let's get some images
  #frames = []
  sys.stdout.write("Grabbing frames:    ")
  sys.stdout.flush()

  num_frames = 25
  for i in range(num_frames):
    ret, frame = cap.read()
    if ret == True:
      # Write the frame into the video file
      out.write(frame)
      #frames.append(frame)
      # Write progress percentage to terminal
      sys.stdout.write("\b\b\b%s%%" % str(int((i+1)/num_frames*100)).rjust(2) )
      sys.stdout.flush()

  sys.stdout.write("\n")
  sys.stdout.flush()

  # Now save them to a file...
  # It eats up memory to append to a lista and then write in a separate task,
  # but it's faster than writing each frame immediately after each read() 
  #sys.stdout.write("Writing frames:    ")
  #sys.stdout.flush()
  #for i, f in enumerate(frames):
  #  out.write(f)
  #  sys.stdout.write("\b\b\b%s%%" % str(int((i+1)/num_frames*100)).rjust(2) )
  #  sys.stdout.flush()

  #sys.stdout.write("\n")
  #sys.stdout.flush()

  # We're done!
  cap.release()
  out.release()
