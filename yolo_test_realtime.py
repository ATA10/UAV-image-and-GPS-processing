import cv2
from ultralytics import YOLO

# Load the YOLO model
model = YOLO('yolomodel/model/detect/train/weights/best.pt')

# Print the class names
print(model.names)

# Initialize the webcam
webcamera = cv2.VideoCapture(0)
webcamera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
webcamera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

frame_count = 0
process_every_n_frames = 5

while True:
    success, frame = webcamera.read()
    
    if not success:
        print("Failed to capture frame from webcam. Exiting...")
        break

    frame_count += 1
    if frame_count % process_every_n_frames != 0:
        cv2.imshow("Live Camera", frame)
        if cv2.waitKey(1) == ord('q'):
            break
        continue
    
    # Run the YOLO model to get tracking results
    results = model.track(frame, classes=0, conf=0.8, imgsz=320)
    
    # Extract the number of boxes detected
    num_boxes = len(results[0].boxes)
    
    # Add text to the frame showing the total number of detections
    cv2.putText(frame, f"Total: {num_boxes}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    
    # Plot the results on the frame
    plotted_frame = results[0].plot()
    
    # Display the frame with detections
    cv2.imshow("Live Camera", plotted_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release the webcam and close all OpenCV windows
webcamera.release()
cv2.destroyAllWindows()