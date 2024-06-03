from flask import Flask, render_template, request, jsonify
import math
import json
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Kuş uçuşu mesafe hesaplama fonksiyonu
def hesapla_kus(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

# Metre olarak mesafe hesaplama fonksiyonu (Haversine)
def hesapla_metre(coord1, coord2):
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    a = math.sin(delta_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371000  # Earth's radius in meters
    distance = R * c
    return distance

@app.route('/sonuc', methods=['POST'])
def sonuc():    
    try:
        marker_data = json.loads(request.form.get('markerData', '[]'))
        rectangle_data = json.loads(request.form.get('rectangleData', '[]'))

        if not marker_data or not rectangle_data:
            return jsonify({"error": "Invalid or missing data"}), 400

        marker_data_list = marker_data[1:]
        rectangle_data_list = rectangle_data[1:]

        sum_x = sum(coord[0] for coord in rectangle_data_list)
        sum_y = sum(coord[1] for coord in rectangle_data_list)
        center_x = sum_x / len(rectangle_data_list)
        center_y = sum_y / len(rectangle_data_list)

        animals_coords = {
            f"animal_coords_{i+1}": {
                "x": coords[0],
                "y": coords[1],
                "name": f"Hayvan{i+1}",
                "temperature": 15 + (i+1) * 2,
                "distance_metre": hesapla_metre((center_x, center_y), coords)
            } for i, coords in enumerate(marker_data_list)
        }

        camera_coords = rectangle_data_list[:4]
        data = {
            "center_x": center_x,
            "center_y": center_y,
            "animal_coords": animals_coords,
            "camera_coords": camera_coords
        }

        with open("output.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        return render_template('sonuc.html', mdList=marker_data_list, rcList=rectangle_data_list, orta_nokta=(center_x, center_y), data=data)
    
    except (json.JSONDecodeError, TypeError) as e:
        return jsonify({"error": str(e)}), 400

@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        if not os.path.exists("output.json"):
            return jsonify({"error": "Data not found"}), 404
        with open("output.json", "r") as json_file:
            data = json.load(json_file)
        return jsonify(data)
    except json.JSONDecodeError:
        return jsonify({"error": "Data corrupted"}), 500

@app.route('/save_coordinates', methods=['POST'])
def save_coordinates():
    data = request.get_json()
    camera_coords = data.get('camera_coords')
    center_coords = data.get('center_coords')

    if not camera_coords or not center_coords:
        return jsonify({"error": "Invalid or missing data"}), 400

    try:
        existing_data = {}
        if os.path.exists('output.json'):
            with open('output.json', 'r') as f:
                existing_data = json.load(f)

        existing_data.update({
            'camera_coords': camera_coords,
            'center_x': center_coords[0],
            'center_y': center_coords[1]
        })

        with open('output.json', 'w') as f:
            json.dump(existing_data, f, indent=4)

        return jsonify({"status": "success"}), 200
    except json.JSONDecodeError:
        return jsonify({"error": "Data corrupted"}), 500

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/gonder', methods=['POST'])
def gonder():
    try:
        data = request.get_json()
        marker_data_list = data["mdList1"]
        rectangle_data_list = data["rectangleCoordinates"]

        sum_x = sum(coord[0] for coord in rectangle_data_list)
        sum_y = sum(coord[1] for coord in rectangle_data_list)
        center_x = sum_x / len(rectangle_data_list)
        center_y = sum_y / len(rectangle_data_list)

        animals_coords = {
            f"animal_coords_{i+1}": {
                "x": coords[0],
                "y": coords[1],
                "name": f"Hayvan{i+1}",
                "temperature": 15 + (i+1) * 2,
                "distance_metre": hesapla_metre((center_x, center_y), coords)
            } for i, coords in enumerate(marker_data_list)
        }

        camera_coords = rectangle_data_list[:4]
        response_data = {
            "center_x": center_x,
            "center_y": center_y,
            "animal_coords": animals_coords,
            "camera_coords": camera_coords
        }

        with open("output.json", "w") as json_file:
            json.dump(response_data, json_file, indent=4)

        return jsonify({"message": "Veriler başarıyla alındı!", "data": response_data})

    except (json.JSONDecodeError, KeyError, TypeError) as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=False)
