#!/usr/bin/env python3
from picamera2 import Picamera2
import time
import base64
import sys # To print to stdout
import io  # To handle in-memory image data

# Get the current user's login name
user = os.getlogin()
# Get the path to the user's home directory
user_home = os.path.expanduser(f'~{user}')

cameras_info = Picamera2.global_camera_info()
print("Available cameras: ",cameras_info)

camera_id_to_use = 0
found_camera = True

for cam_info in cameras_info:
    if cam_info['Num'] == camera_id_to_use:
        found_camera = True

if found_camera:
    try:
        camera = Picamera2(0)
        cam_config = camera.create_still_configuration(main={"size":(1920,1080)})#
        camera.configure(cam_config)
        
        # Start the camera
        camera.start()
        
        buffer = io.BytesIO()
        camera.capture_file(buffer, format="jpeg") # Capture directly to the buffer as JPEG
        buffer.seek(0) # Rewind the buffer to the beginning

        # Read the image data from the buffer
        image_data = buffer.read()

        # Stop the camera to release resources
        camera.stop()

        # --- Encode image data to Base64 ---
        encoded_image = base64.b64encode(image_data).decode('utf-8')

        # --- Output the Base64 string to standard output (stdout) ---
        print(encoded_image)

    except KeyboardInterrupt:
        # Stop the cameraif a KeyboardInterrupt (e.g., Ctrl+C) occurs
        camera.stop()
        pass
    except Exception as e:
        # Print errors to stderr so Node-RED can capture them in msg.payload.stderr
        print(f"An error occurred: {e}", file=sys.stderr)
        # Ensure camera is stopped if an error occurs after starting
        if 'picam2' in locals() and picam2.started:
            picam2.stop()
        sys.exit(1) # Exit with an error code
else:
    print("camera not found")