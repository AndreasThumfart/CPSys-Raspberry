import os
import time
import base64
import json
import io
import sys
from picamera2 import Picamera2

# --- Camera Configuration (adjust as needed) ---
SAVE_DIRECTORY = "/tmp/" # Still use /tmp/ for temporary storage during capture
IMAGE_FILENAME_PREFIX = "capture_"
IMAGE_FORMAT = "jpeg"
IMAGE_RESOLUTION = (1920, 1080) # Full HD, adjust as needed

def capture_image_data(camera_num):
    """
    Captures an image from a specific camera and returns its Base64 encoded data
    along with metadata.
    Returns None if an error occurs.
    """
    picam2 = None
    filename = None
    try:
        picam2 = Picamera2(camera_num=camera_num)

        camera_config = picam2.create_still_configuration(
            main={"size": IMAGE_RESOLUTION}
        )
        picam2.configure(camera_config)

        picam2.start()
        #time.sleep(1) # Give camera time to set exposure

        timestamp = time.strftime("%Y%m%d-%H%M%S")

        print(f"Capturing image from Camera {camera_num}", file=sys.stderr, flush=True)
        buffer = io.BytesIO()
        picam2.capture_file(buffer, format=IMAGE_FORMAT) # Capture directly to the buffer as JPEG
        buffer.seek(0) # Rewind the buffer to the beginning
        # Read the image data from the buffer
        image_data = buffer.read()
        print(f"Image captured from Camera {camera_num}", file=sys.stderr, flush=True)

        picam2.stop()

        base64_encoded_image = base64.b64encode(image_data).decode('utf-8')

        return {
            "timestamp": timestamp,
            "camera_id": camera_num,
            "format": IMAGE_FORMAT,
            "resolution": f"{IMAGE_RESOLUTION[0]}x{IMAGE_RESOLUTION[1]}",
            "image_data": base64_encoded_image
        }

    except Exception as e:
        print(f"Error capturing image from Camera {camera_num}: {e}", file=sys.stderr, flush=True)
        return None # Indicate failure
    finally:
        if picam2 and picam2.started:
            picam2.stop()
        if filename and os.path.exists(filename):
            os.remove(filename)
            # print(f"Temporary file {filename} removed.", flush=True)

def main():
    all_camera_data = [] # List to hold data for both cameras

    # --- Camera Detection Logic ---
    cameras_info = Picamera2.global_camera_info()
    print("Available cameras information:", cameras_info, file=sys.stderr, flush=True)

    detected_camera_nums = []
    for cam_info in cameras_info:
        if 'Num' in cam_info:
            detected_camera_nums.append(cam_info['Num'])
        elif 'id' in cam_info: # Fallback for 'id' if 'Num' is not present
            detected_camera_nums.append(cam_info['id'])
        # If no explicit 'Num' or 'id', and it's the first in the list
        elif not detected_camera_nums and len(cameras_info) == 1:
            detected_camera_nums.append(0)

    if not detected_camera_nums:
        print("No cameras detected by Picamera2.global_camera_info().", file=sys.stderr, flush=True)
        # Output a JSON indicating no cameras found
        json.dump({"status": "error", "message": "No cameras detected"}, sys.stdout)
        return

    detected_camera_nums.sort()
    # print(f"Detected camera numbers: {detected_camera_nums}", flush=True)

    # --- Capture and Collect for Each Detected Camera ---
    for cam_num in detected_camera_nums:
        data = capture_image_data(cam_num)
        if data:
            all_camera_data.append(data)
        time.sleep(2) # Short delay between captures

    # --- Output JSON to stdout ---
    # Dump the list of camera data dictionaries as a single JSON array to stdout
    #json.dump(all_camera_data, sys.stdout)
    print(json.dumps(all_camera_data), flush=True) # Ensure it flushes immediately

if __name__ == "__main__":
    main()