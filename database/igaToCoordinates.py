import json
from geopy.geocoders import Nominatim
from time import sleep

# Load the JSON file
with open('./sudo/LGA-P29_Number_of_Motor_Vehicle_by_Dwelling-Census_2016.json/lga_p29_number_motor_vehicles_by_dwelling_census_2016-7363434778523901620.json', 'r') as file:
    data = json.load(file)

# Initialize the geolocator
geolocator = Nominatim(user_agent="UniqueAppNameForProject")

# Empty dictionary to store coordinates
coordinates = {}

# Iterate through each feature in the JSON file
for feature in data['features']:
    lga_name = feature['properties']['lga_name16']
    try:
        # Geocode the LGA name
        location = geolocator.geocode(lga_name + ', Victoria, Australia', timeout=10)
        if location:
            coordinates[lga_name] = (location.latitude, location.longitude)
        else:
            coordinates[lga_name] = 'Coordinates not found'
        print(f'{lga_name}: Latitude = {location.latitude if location else "Not found"}, Longitude = {location.longitude if location else "Not found"}')
    except Exception as e:
        print(f'Error processing {lga_name}: {str(e)}')
    sleep(1)  # Sleep to avoid hitting API limits

# Optionally, save the results to a file
with open('lga_coordinates.json', 'w') as outfile:
    json.dump(coordinates, outfile, indent=4)
