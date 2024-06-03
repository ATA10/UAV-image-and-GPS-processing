import cv2
import numpy as np
import random
import json


class VideoProcessor:
    def __init__(self, video_file, target_width, target_height, num_animals):
        self.video_file = video_file
        self.target_width = target_width
        self.target_height = target_height
        self.cap = cv2.VideoCapture(video_file)
        self.animals = self.create_animals(num_animals)
        self.corners = None

        with open('output.json', 'r') as f:
            data = json.load(f)
            camera_coords = data['camera_coords'][:4]
            self.corners = {
                'top_left': tuple(camera_coords[0]),
                'top_right': tuple(camera_coords[1]),
                'bottom_left': tuple(camera_coords[2]),
                'bottom_right': tuple(camera_coords[3])
            }
        
        self.cornerspixel = {
            'top_leftpixel': (150, 170),
            'top_rightpixel': (1400, 170),
            'bottom_leftpixel': (150, 920),
            'bottom_rightpixel': (1400, 920)
        }

    def create_animals(self, num_animals):
        animals = []
        with open('output.json', 'r') as f:
            data = json.load(f)
            animal_coords = data['animal_coords']
            for i in range(num_animals):
                animal_name = f'Animal{i+1}'
                random_animal_key = f'animal_coords_{random.randint(1, len(animal_coords))}'
                random_animal = animal_coords[random_animal_key]
                animal = {
                    'name': animal_name,
                    'size': 20,
                    'x': random.randint(0, self.target_width - 20),
                    'y': random.randint(0, self.target_height - 20),
                    'color': (0, 255, 0),
                    'coordinates': random_animal
                }
                animals.append(animal)
                print(f'{animal_name} coordinates: {random_animal}')
        return animals

    def process_video(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            original_height, original_width = frame.shape[:2]
            background = np.zeros((self.target_height, self.target_width, 3), dtype=np.uint8)
            x_offset = (self.target_width - original_width) // 2
            y_offset = (self.target_height - original_height) // 2
            background[y_offset:y_offset + original_height, x_offset:x_offset + original_width] = frame

            for animal in self.animals:
                animal_center_x = animal['x'] + animal['size'] // 2
                animal_center_y = animal['y'] + animal['size'] // 2

                self.draw_animal(background, animal['x'], animal['y'])
                self.draw_arrow_if_needed(background, animal, x_offset, y_offset, original_width, original_height)
            self.draw_corners(background)
            cv2.imshow('Video', background)
            if cv2.waitKey(25) & 0xFF == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def draw_corners(self, background):
        for corner_name_pixel, corner_pos_pixel in self.cornerspixel.items():
            corner_name = corner_name_pixel.replace("pixel", "")
            corner_pos = self.corners[corner_name]
            text = f"{corner_pos}"
            cv2.putText(background, text, corner_pos_pixel, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    def draw_animal(self, background, x, y):
        cv2.rectangle(background, (x, y), (x + 20, y + 20), (0, 255, 0), -1)

    def draw_arrow_if_needed(self, background, animal, x_offset, y_offset, original_width, original_height):
        x = animal['x']
        y = animal['y']
        if any((
            x < x_offset,
            x + 20 > x_offset + original_width,
            y < y_offset,
            y + 20 > y_offset + original_height
        )):
            arrow_start_x = max(min(x + 20 // 2, x_offset + original_width - 50), x_offset + 50)
            arrow_start_y = max(min(y + 20 // 2, y_offset + original_height - 50), y_offset + 50)

            if x < x_offset:
                arrow_end_x = x_offset
            elif x + 20 > x_offset + original_width:
                arrow_end_x = x_offset + original_width - 1
            else:
                arrow_end_x = x + 20 // 2

            if y < y_offset:
                arrow_end_y = y_offset
            elif y + 20 > y_offset + original_height:
                arrow_end_y = y_offset + original_height - 1
            else:
                arrow_end_y = y + 20 // 2

            arrow_end = (arrow_end_x, arrow_end_y)

            cv2.arrowedLine(background, (arrow_start_x, arrow_start_y), arrow_end, (255, 255, 255), 2)

            distance_x = abs(arrow_end_x - (x + 20 // 2))
            distance_y = abs(arrow_end_y - (y + 20 // 2))
            animal_distance = round(np.sqrt(distance_x ** 2 + distance_y ** 2), 2)

            cv2.putText(background, f"{animal['name']} Distance: {animal_distance}",
                        (arrow_end_x + 10, arrow_end_y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

if __name__ == "__main__":
    video_file = "videos/ornek_video.mp4"
    # video_file = 0
    target_width = 1920
    target_height = 1080
    num_animals = 5

    video_processor = VideoProcessor(video_file, target_width, target_height, num_animals)
    video_processor.process_video()
