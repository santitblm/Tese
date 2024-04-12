import gpxpy
import gpxpy.gpx

# Parsing an existing file:
# -------------------------

gpx_file = open('RandomCodigos/code_for_GPS/2024-04-09_9_Apr_2024_15_58_50.gpx', 'r')

gpx = gpxpy.parse(gpx_file)

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            print(f'Point at ({point.latitude},{point.longitude}) -> {point.elevation}, at time {point.time}')

#for waypoint in gpx.waypoints:
#    print(f'waypoint {waypoint.name} -> ({waypoint.latitude},{waypoint.longitude})')

#for route in gpx.routes:
#    print('Route:')
#    for point in route.points:
#        print(f'Point at ({point.latitude},{point.longitude}) -> {point.elevtion}')

# There are many more utility methods and functions:
# You can manipulate/add/remove tracks, segments, points, waypoints and routes and
# get the GPX XML file from the resulting object:

#print('GPX:', gpx.to_xml())

# Creating a new file:
# --------------------

#gpx = gpxpy.gpx.GPX()

# Create first track in our GPX:
#gpx_track = gpxpy.gpx.GPXTrack()
#gpx.tracks.append(gpx_track)

# Create first segment in our GPX track:
#gpx_segment = gpxpy.gpx.GPXTrackSegment()
#gpx_track.segments.append(gpx_segment)

# Create points:
#gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(2.1234, 5.1234, elevation=1234))
#gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(2.1235, 5.1235, elevation=1235))
#gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(2.1236, 5.1236, elevation=1236))

# You can add routes and waypoints, too...

#print('Created GPX:', gpx.to_xml())


