import folium
import gpxpy
#from folium.plugins import ColorLine

# Open the GPX file
gpx_file = open('RandomCodigos/code_for_GPS/2024-04-12_12_04_2024_09_44_09.gpx', 'r')

# Parse the GPX data
gpx = gpxpy.parse(gpx_file)

# Create a map centered around the first point
map_center = [gpx.tracks[0].segments[0].points[0].latitude, gpx.tracks[0].segments[0].points[0].longitude]
map = folium.Map(location=map_center, zoom_start=15)

# Define a color scale for elevation changes
min_elevation = min(point.elevation for track in gpx.tracks for segment in track.segments for point in segment.points)
max_elevation = max(point.elevation for track in gpx.tracks for segment in track.segments for point in segment.points)

def get_color(elevation):
    normalized_elevation = (elevation - min_elevation) / (max_elevation - min_elevation)
    # Choose color based on elevation (adjust this to your preference)
    if normalized_elevation < 0.33:
        return 'green'
    elif normalized_elevation < 0.66:
        return 'orange'
    else:
        return 'red'

# Add markers for each point with color based on elevation
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            color = get_color(point.elevation)
            folium.Marker(location=[point.latitude, point.longitude], icon=folium.Icon(color=color), popup=f'Elevation: {point.elevation}, Time: {point.time}').add_to(map)


maps_destination_folder = '/home/santilm/Desktop/Mapas' # Não pode ter / no fim

# Save the map to an HTML file
map.save(f'{maps_destination_folder}/map_with_colored_points.html')