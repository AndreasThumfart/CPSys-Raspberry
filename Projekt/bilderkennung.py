from ultralytics import YOLO
#import cv2
#import pandas as pd
import sys
import json




# Funktion zur Zählung der Personen auf einem Bild
def count_persons(image_path, model):
    print(f"image processing started for {image_path} ", file=sys.stderr, flush=True)
    results = model(image_path)
    person_count = 0
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls)
            if class_id == 0:  # 0 ist die Klassen-ID für Personen in COCO
                person_count += 1
    print(f"image processing completed for {image_path}, result {person_count} ", file=sys.stderr, flush=True)
    return person_count

# Auswertung der Bilder
def get_video_id(personCount):
    match personCount:
        case num if num <  6:
            return 1
        case num if 6 <= num < 11:
            return 2
        case num if num > 11:
            return 3
        case _:
            return None

def main():
    try:
        # Lade das YOLOv8-Modell
        model = YOLO('yolov8n.pt')

        print("image recognition started", file=sys.stderr, flush=True)
        sys.stderr.write("test")


        #fileinfos = "[{\"filename\":\"C:/Projekte/20250613-154712_camera0.jpeg\",\"cameraid\":0},{\"filename\":\"C:/Projekte/20250613-154715_camera1.jpeg\",\"cameraid\":1}]"
        fileinfos = sys.argv[1]
        print(f"file paths information object: {fileinfos}",file=sys.stderr, flush=True)
        incoming_data = json.loads(fileinfos)

        wagons = []

        for fileinfo in incoming_data:
            camera_id = fileinfo["cameraid"]
            filename = fileinfo["filename"]

            personCount = count_persons(filename,model)
            wagon = {
                "id" : camera_id+1,
                "videoId" : get_video_id(personCount)
            }
            wagons.append(wagon)

        print(json.dumps(wagons), file=sys.stdout, flush=True)

    except Exception as e:
        print(f"Error processing images: {e}", file=sys.stderr, flush=True)
    finally:
        print("image analysis complete", file=sys.stderr, flush=True)
#get_video_ids(person_count_1, person_count_2, excel_data)

if __name__ == "__main__":
    main()

