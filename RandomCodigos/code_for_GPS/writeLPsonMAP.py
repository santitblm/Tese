import gpxpy
from datetime import datetime, timezone, timedelta
import math
import folium

def get_bearing(lat1, lon1, lat2, lon2):
    """
    Calculate the bearing between two points.
    """
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1

    y = math.sin(dlon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)

    return math.degrees(math.atan2(y, x))

def get_destination_point(lat, lon, bearing, distance):
    """
    Calculate the destination point given a starting point, bearing, and distance.
    """
    R = 6371.0  # Earth radius in kilometers

    lat1 = math.radians(lat)
    lon1 = math.radians(lon)
    bearing = math.radians(bearing)

    lat2 = math.asin(math.sin(lat1) * math.cos(distance / R) +
                     math.cos(lat1) * math.sin(distance / R) * math.cos(bearing))
    lon2 = lon1 + math.atan2(math.sin(bearing) * math.sin(distance / R) * math.cos(lat1),
                              math.cos(distance / R) - math.sin(lat1) * math.sin(lat2))

    return math.degrees(lat2), (math.degrees(lon2) + 540) % 360 - 180  # Normalize longitude to [-180, 180]



# Read the GPX file
gpx_file = open('RandomCodigos/code_for_GPS/2024-04-10_10_Apr_2024_17_36_58.gpx', 'r')
gpx = gpxpy.parse(gpx_file)

videos = [
    {"video": "20240410_173631866.MOV", "side": "R"},
    {"video": "20240410_173628966.MOV", "side": "L"}
]

# Create a list to store tuples of (timestamp, latitude, longitude)
points_data = []

# Iterate through the GPX data and populate the list
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            points_data.append((point.time.replace(tzinfo=timezone.utc), point.latitude, point.longitude))

# Read the text file with codes and timestamps
codes_and_positions = []
for video_info in videos:
    video = video_info["video"]
    side = video_info["side"]

    predictions_file = f'/home/santilm/Desktop/Results_LPDet+OCR/{video}/predictions.txt'
    calendar = f"{video[:4]}-{video[4:6]}-{video[6:8]} "

    with open(predictions_file, 'r') as file:
        lines = file.readlines()

    # Replace timestamps with corresponding latitudes and longitudes
    for line in lines:
        code, timestamp = line.strip().split()  # Assuming the side is specified in the text file
        timestamp = calendar + timestamp
        timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S:%f').replace(tzinfo=timezone(timedelta(hours=1)))  # Make the timestamp aware of timezone

        # Find the closest points in the GPX data
        points_data.sort(key=lambda p: abs((p[0] - timestamp).total_seconds()))

        # Linear interpolation
        for i in range(len(points_data) - 1):
            if points_data[i][0] <= timestamp <= points_data[i + 1][0]:
                t1, lat1, lon1 = points_data[i]
                t2, lat2, lon2 = points_data[i + 1]
                time_diff = (timestamp - t1).total_seconds()
                total_diff = (t2 - t1).total_seconds()
                ratio = time_diff / total_diff
                latitude = lat1 + (lat2 - lat1) * ratio
                longitude = lon1 + (lon2 - lon1) * ratio

                # Get the bearing of the trajectory at this point
                bearing = get_bearing(lat1, lon1, lat2, lon2)

                # Calculate the position slightly to the left or right of the trajectory
                if side == "R":
                    new_lat, new_lon = get_destination_point(latitude, longitude, bearing + 90, 0.005)  # Change distance as needed
                elif side == "L":
                    new_lat, new_lon = get_destination_point(latitude, longitude, bearing - 90, 0.005)  # Change distance as needed
                else:
                    new_lat, new_lon = latitude, longitude  # Use original position if side is not specified or invalid

                codes_and_positions.append((code, new_lat, new_lon))
                print(f"Code: {code}, Latitude: {latitude}, Longitude: {longitude}")
                break


# Create a map centered around the mean latitude and longitude
map_center = [sum(p[1] for p in codes_and_positions) / len(codes_and_positions),
              sum(p[2] for p in codes_and_positions) / len(codes_and_positions)]
mymap = folium.Map(location=map_center, zoom_start=19)

# Add markers for each code at its corresponding position
for code, lat, lon in codes_and_positions:
    folium.Marker([lat, lon], popup=code).add_to(mymap)

maps_destination_folder = '/home/santilm/Desktop/Mapas' # Não pode ter / no fim

# Save the map to an HTML file
mymap.save(f'{maps_destination_folder}/map_{video.split(".MOV")[0][:-3]}.html')

