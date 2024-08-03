# UAV Live Animal Detection

This project aims to track and monitor wild animals using UAV (Unmanned Aerial Vehicle) cameras. It involves advanced image processing techniques to detect and visualize animals' positions within the UAV camera's field of view.

## Project Overview

The main objective is to locate and track animals within a UAV image and visualize their positions. If an animal is outside the UAV image, a cursor indicates its position and distance.

### Key Features
- **Real-Time Animal Tracking**: Detects and tracks animals in real-time using UAV camera imagery.
- **Distance Calculation**: Calculates the distance of animals from the UAV camera considering Earth's tilt, axis, and shape.
- **Visualization**: Displays animals' positions within the image or indicates their positions and distances if outside the image frame.
- **Web-Based Simulation**: Uses Python's Flask library for a web-based simulation of UAV camera and animal positions.
- **YOLOv8 Model**: Employs the YOLOv8 model for high-performance animal detection and classification.

## Installation

1. Clone the repository:
   git clone https://github.com/ATA10/UAV-image-and-GPS-processing
   cd UAV-Live-Animal-Detection

2. Create a virtual environment and activate it:
   `python3 -m venv env`
   `source env/bin/activate`   # On Windows use `env\Scripts\activate`

## Usage

1. Start the web application:
   python testdatas.py
   
2. Access the application in your web browser at `http://localhost:5000`,and once you have selected how many animals you will have, edited the position of the rectangle and calculated the distances, you can start testing, this file is used to create simulation coordinates

3. Start the Video Processor
   If you want the use video processor without Real-time Yolo model:
     `python videoproc_v3_video.py`
   If you want the use video processor with Real-Time Yolo Detection Model:
     `python videoproc_v4_realtime.py`
   
## Project Structure

- `testdatas.py`: The main Flask application file.
- `models/`: Directory containing the trained YOLOv8 model.
- `static/` and `templates/`: Directories for the web application's static files and templates.
- `videoproc_v3_video.py`: Script for processing GPS and sensor data. Also old version have another algorithm and technic in repository 
- `yolo_test_video.py`: Script for detecting and visualizing animals in UAV images.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## Contact

For any questions or inquiries, please contact the project contributors:
- Anıl Taha ADAK: tahaadak94@gmail.com
- Alperen KARSLI: alperenkarsliceng@gmail.com
- Asil FINDIK: asilfndk@gmail.com

Academic Advisor: Doç. Dr. Fatih AYDIN
Industrial Advisor: Dr. Muhterem Özgür KIZILKAYA
