import json
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    a = sin(dLat/2) * sin(dLat/2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon/2) * sin(dLon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            return None  # or return date_str if you want to keep the original on error

# Load data from JSON files
with open('./Melbourne_house_price-2016-2018/Melbourne_house_price.json', 'r') as file:
    properties_data = json.load(file)

with open('./climateStation/all_sites.json', 'r') as file:
    sites_data = json.load(file)['records']

results = []

for i, property in enumerate(properties_data):
    lat = property.get('Lattitude')
    lon = property.get('Longtitude')
    min_distance = float('inf')
    closest_site_id = None

    if lat and lon:
        for site in sites_data:
            site_coords = site['geometry']['coordinates']
            distance = haversine(lat, lon, site_coords[0], site_coords[1])
            if distance < min_distance:
                min_distance = distance
                closest_site_id = site['siteID']

    formatted_date = format_date(property.get('Date', ''))  # Format the date

    result = {
        "id": i,
        "suburb": property.get('Suburb', ''),
        "address": property.get('Address', ''),
        "price": property.get('Price', None) or None,
        "date": formatted_date,  # Use the formatted date
        "distance": property.get('Distance', None) or None,
        "postcode": property.get('Postcode', None) or None,
        "latitude": lat,
        "longitude": lon,
        "station_id": closest_site_id or "Location not found"
    }
    results.append(result)

# Save results to a JSON file
with open('housePriceFinalData.json', 'w') as f:
    json.dump(results, f, indent=4)

print("Completed processing all data.")
