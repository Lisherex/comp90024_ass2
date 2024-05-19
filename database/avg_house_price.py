import json
from math import radians, sin, cos, sqrt, atan2
import collections

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    a = sin(dLat/2) * sin(dLat/2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon/2) * sin(dLon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

# Load data from JSON files
with open('./Melbourne_house_price-2016-2018/Melbourne_house_price.json', 'r') as file:
    properties_data = json.load(file)

with open('./climateStation/all_sites.json', 'r') as file:
    sites_data = json.load(file)['records']

# Dictionary to hold the sum of prices and count of properties for each station
station_prices = collections.defaultdict(lambda: {'sum': 0, 'count': 0})

for property in properties_data:
    lat = property.get('Lattitude')
    lon = property.get('Longtitude')
    price = property.get('Price')  # Assuming the key for house price is 'Price'
    min_distance = float('inf')
    closest_site_id = None

    if lat and lon and price:
        for site in sites_data:
            site_coords = site['geometry']['coordinates']
            distance = haversine(lat, lon, site_coords[0], site_coords[1])
            if distance < min_distance:
                min_distance = distance
                closest_site_id = site['siteID']

        # Aggregate prices by station_id
        if closest_site_id:
            station_prices[closest_site_id]['sum'] += price
            station_prices[closest_site_id]['count'] += 1

# Calculate average prices
average_prices = {station_id: price_data['sum'] / price_data['count'] for station_id, price_data in station_prices.items() if price_data['count'] > 0}

# Append average prices to results with id
results = []
for idx, (station_id, average_price) in enumerate(average_prices.items()):
    results.append({
        "id": idx,
        "station_id": station_id,
        "average_price": average_price
    })

# Save results to a JSON file
with open('avg_house_price.json', 'w') as f:
    json.dump(results, f, indent=4)

print("Completed processing all data.")
