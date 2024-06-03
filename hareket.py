import json
import random
import time
import math

def hesapla_metre(coord1, coord2):
    # Dereceleri radyanlara dönüştür
    lat1 = math.radians(coord1[0])
    lon1 = math.radians(coord1[1])
    lat2 = math.radians(coord2[0])
    lon2 = math.radians(coord2[1])

    # İki nokta arasındaki enlem ve boylam farkını hesapla
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    # Haversine formülünü kullanarak uzaklığı hesapla
    a = math.sin(delta_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371000  # Earth's radius in meters
    distancem = R * c

    return distancem

def move_animals(animal_coords, center_x, center_y):
    for animal_id, animal_info in animal_coords.items():
        # Rastgele x ve y yönlere 10 metre hareket ettir
        animal_info["x"] += random.uniform(-0.00009, 0.000009)
        animal_info["y"] += random.uniform(-0.00009, 0.000009)
        
        # Merkeze olan uzaklığı hesapla
        distance = hesapla_metre([animal_info["x"], animal_info["y"]], [center_x, center_y])
        # distance_metre alanını güncelle
        animal_info["distance_metre"] = distance
        
        print(f"{animal_info['name']} konumu güncellendi: ({animal_info['x']}, {animal_info['y']})")

    return animal_coords

def write_to_json(data):
    with open("output.json", "w") as f:
        json.dump(data, f, indent=4)

def main():
    with open("output.json", "r") as f:
        data = json.load(f)

    center_x = data["center_x"]
    center_y = data["center_y"]

    while True:
        data["animal_coords"] = move_animals(data["animal_coords"], center_x, center_y)
        write_to_json(data)
        time.sleep(5)  # 5 saniye bekle

if __name__ == "__main__":
    main()
