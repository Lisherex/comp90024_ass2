import json
from geopy.geocoders import Nominatim
from time import sleep
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    a = sin(dLat/2) * sin(dLat/2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon/2) * sin(dLon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

# Load LGA and site data
with open('./sudo/LGA-P29_Number_of_Motor_Vehicle_by_Dwelling-Census_2016.json/lga_p29_number_motor_vehicles_by_dwelling_census_2016-7363434778523901620.json', 'r') as file:
    lga_data = json.load(file)['features']

with open('./climateStation/all_sites.json', 'r') as file:
    sites_data = json.load(file)['records']

# Initialize the geolocator
geolocator = Nominatim(user_agent="UniqueAppNameForProject")

# Prepare the output dictionary
output_data = []

for feature in lga_data:
    lga_properties = feature['properties']
    lga_name = lga_properties['lga_name16']
    try:
        location = geolocator.geocode(lga_name + ', Victoria, Australia', timeout=10)
        if location:
            min_distance = float('inf')
            closest_site_id = None
            for site in sites_data:
                site_coords = site['geometry']['coordinates']
                distance = haversine(location.latitude, location.longitude, site_coords[0], site_coords[1])
                if distance < min_distance:
                    min_distance = distance
                    closest_site_id = site['siteID']
            output_data.append({
                "id": feature['id'],
                "lga_code": lga_properties['lga_code_2016'],
                "lga_name": lga_name,
                "station_id": closest_site_id,
                "none_vehicle_per_dwelling": lga_properties['num_mvs_per_dweling_0_mvs'],
                "one_vehicle_per_dwelling": lga_properties['num_mvs_per_dweling_1_mvs'],
                "two_vehicle_per_dwelling": lga_properties['num_mvs_per_dweling_2_mvs'],
                "three_vehicle_per_dwelling": lga_properties['num_mvs_per_dweling_3_mvs'],
                "more_than_four_vehicle_per_dwelling": lga_properties['num_mvs_per_dweling_4mo_mvs'],
                "total_dwelling": lga_properties['total_dwelings']
            })
        else:
            output_data.append({
                "id": feature['id'],
                "lga_code": lga_properties['lga_code_2016'],
                "lga_name": lga_name,
                "station_id": "Location not found",
                "none_vehicle_per_dwelling": lga_properties['num_mvs_per_dweling_0_mvs'],
                "one_vehicle_per_dwelling": lga_properties['num_mvs_per_dweling_1_mvs'],
                "two_vehicle_per_dwelling": lga_properties['num_mvs_per_dweling_2_mvs'],
                "three_vehicle_per_dwelling": lga_properties['num_mvs_per_dweling_3_mvs'],
                "more_than_four_vehicle_per_dwelling": lga_properties['num_mvs_per_dweling_4mo_mvs'],
                "total_dwelling": lga_properties['total_dwelings']
            })
    except Exception as e:
        print(f'Error processing {lga_name}: {str(e)}')
    sleep(1)  # Respect API limits

# Save the results to a file
with open('vehicleFinalData.json', 'w') as outfile:
    json.dump(output_data, outfile, indent=4)
