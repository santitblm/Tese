from openalpr import Alpr

# Path to the image file
image_path = 'datasets/License_Plates/Cropped/0ACP-FB-1200-NOVAS-MATRICULAS-2021.jpg'

# Create an instance of the Alpr class
alpr = Alpr("us", "/etc/openalpr/openalpr.conf", "openalpr/runtime_data/")

# If the initialization is successful
if alpr.is_loaded():
    # Recognize license plates in the image
    results = alpr.recognize_file(image_path)

    # Print the results
    for plate in results['results']:
        print("Plate: ", plate['plate'])
        print("Confidence: ", plate['confidence'])
        print("")

# Unload the Alpr instance
alpr.unload()