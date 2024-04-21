import os
from math import radians, sin, cos, sqrt, atan2
import numpy as np

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth specified in radians.
    """
    # Radius of the Earth in meters
    R = 6371000.0
    
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance

def stayed_result(coords_before, coords_after, d=10):
    """
    Check if the distance between coords_before and coords_after
    is less than d meters.
    """

    lat1, lon1 = coords_before
    lat2, lon2 = coords_after

    distance = haversine(lat1, lon1, lat2, lon2)

    return distance <= d


def read_LPs_fromHTML(file_path):
    '''
    Open the HTML file (map) and return the results 
    as a set with all the LPs present on the map.
    '''

    with open(file_path, "r") as file:
        html_content = file.read()
    # Parse the HTML
    result = html_content.split('style="width: 100.0%; height: 100.0%;">')

    LPs = []

    for entry in result:
        LP = entry.split("</div>")[0]
        if len(LP) == 6:
            LPs.append(LP)
    return set(LPs)

def get_coords(LP, file_path):
    '''
    Given an LP and the HTML file (map), return the
    coordinates of that LP as a floats numpy array.
    '''

    with open(file_path, "r") as file:  
        html_content = file.read()

    coords_str = html_content.split(LP)[0].split("],\n                {}\n            ).addTo(map_")[-2].split("L.marker(\n                [")[-1]

    coords = coords_str.split(", ")
    return np.array(coords, dtype=float)

# Load the HTML file

directory = "/home/santilm/Desktop/Mapas"

file_path_before = os.path.join(directory, "map_20240416_124743.html")
file_path_after = os.path.join(directory, "map_20240416_144935.html")

LPs_before = read_LPs_fromHTML(file_path_before)
LPs_after = read_LPs_fromHTML(file_path_after)

left = len(LPs_before - LPs_after)
entered = len(LPs_after - LPs_before)

stayed = 0
changed = 0

stayed_changed_LPs = LPs_before.intersection(LPs_after)


for LP in stayed_changed_LPs:

    coords_before = get_coords(LP, file_path_before)
    coords_after = get_coords(LP, file_path_after)

    if stayed_result(coords_before, coords_after):
        stayed += 1
    else:
        changed += 1
    
print(f"Number of cars that:\nLeft: {left}\nEntered: {entered}\nChanged: {changed}\nStayed: {stayed}")
