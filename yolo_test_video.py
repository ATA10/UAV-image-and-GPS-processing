import cv2
from ultralytics import YOLO
import os

def detect_objects_in_video(input_video_path):
    # Check if the input video file exists
    if not os.path.isfile(input_video_path):
        print(f"Error: The input video file '{input_video_path}' does not exist.")
        return

    # Load the YOLOv8 model
    model = YOLO('yolomodel/model/detect/train/weights/best.pt')

    # Initialize the video capture
    video = cv2.VideoCapture(input_video_path)

    if not video.isOpened():
        print(f"Error: Couldn't read video stream from file '{input_video_path}'.")
        return

    while video.isOpened():
        success, frame = video.read()
        
        if not success:
            print("Finished processing video.")
            break

        # Run the YOLOv8 model to get detection results
        results = model(frame)
        
        # Extract the results
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = box.conf[0]

                # Draw the box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Display the confidence
                cv2.putText(frame, f'{confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the frame with detections
        cv2.imshow("YOLO", frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    # Release everything when done
    video.release()
    cv2.destroyAllWindows()

# Run the function with the input video path
input_video_path = 'videos/testvideo.mp4'  # Replace with your input video path
detect_objects_in_video(input_video_path)
