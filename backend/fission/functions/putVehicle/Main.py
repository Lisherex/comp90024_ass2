import os
import json
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers
import urllib.request
import urllib.parse
from Config import Config
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime

load_dotenv()

ELASTIC_SEARCH_URL = os.getenv('ELASTIC_SEARCH_URL')
ELASTIC_SEARCH_PORT = os.getenv('ELASTIC_SEARCH_PORT')
K8S_PERM_RESOURCE_URL = os.getenv('K8S_PERM_RESOURCE_URL')
K8S_PERM_RESOURCE_PORT = os.getenv('K8S_PERM_RESOURCE_PORT')
ES_USERNAME = os.getenv('ES_USERNAME')
ES_PASSWORD = os.getenv('ES_PASSWORDc')

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    a = sin(dLat/2) * sin(dLat/2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon/2) * sin(dLon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c



class K8S_Data:
    # def __init__(self, hdr: dict, baseURL) -> None:
    def __init__(self) -> None:
        # self.hdr = hdr
        # self.baseURL = baseURL
        pass

    @staticmethod
    def constructURL(baseURL, params: dict) -> str:
        queryString = urllib.parse.urlencode(params)

        return f"{baseURL}?{queryString}"

    @staticmethod
    def getData(baseURL: str, params: dict, hdr: dict) -> dict:
        url = f"{baseURL}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers=hdr)

        try:
            with urllib.request.urlopen(req) as response:
                resBody = response.read().decode("utf-8")
                data = json.loads(resBody)
                # Initialize the geolocator
                geolocator = Nominatim(user_agent="UniqueAppNameForProject")

                # Prepare the output dictionary
                output_data = []

                # Load LGA and site data
                with open('./sudo/LGA-P29_Number_of_Motor_Vehicle_by_Dwelling-Census_2016.json/lga_p29_number_motor_vehicles_by_dwelling_census_2016-7363434778523901620.json', 'r') as file:
                    lga_data = json.load(file)['features']

                with open('./climateStation/all_sites.json', 'r') as file:
                    sites_data = json.load(file)['records']
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
            return output_data
        except urllib.error.HTTPError as e:
            print(f"HTTP error occurred: {e.code} {e.reason}")
            raise
        except urllib.error.URLError as e:
            print(f"URL error occurred: {e.reason}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

def updateFunc():
    configLoader = Config(True)
    secretLoader = Config(False)


    try:
        data = K8S_Data.getData(
            baseURL=configLoader("k8s-urls", "K8S_PERM_RESOURCE_URL")
        )
    except urllib.error.HTTPError as e:
        print(f"Handled HTTP error: {e.code} {e.reason}")
        raise
    except urllib.error.URLError as e:
        print(f"Handled URL error: {e.reason}")
        raise
    except Exception as e:
        print(f"Handled unexpected error: {e}")
        raise

    return data


def updateFuncLocal():

    try:
        data = K8S_Data.getData(
            baseURL=K8S_PERM_RESOURCE_URL
        )
    except urllib.error.HTTPError as e:
        print(f"Handled HTTP error: {e.code} {e.reason}")
        raise
    except urllib.error.URLError as e:
        print(f"Handled URL error: {e.reason}")
        raise
    except Exception as e:
        print(f"Handled unexpected error: {e}")
        raise

    # return data


    url = ELASTIC_SEARCH_URL
    port = ELASTIC_SEARCH_PORT
    username = ES_USERNAME
    password = ES_PASSWORD
    es = Elasticsearch(f"{url}:{port}",
                       verify_certs=False,
                       basic_auth=(username, password)
                       )
    del url, port, username, password
    info = es.info().body
    # return info

    with open('./../../database/housePriceFinalData.json', 'r') as file:
        house_price_data = json.load(file)

    for index, house_price in enumerate(house_price_data):
        house_price['_index'] = INDEX_NAME

    response = bulk(client, house_price_data)
    return response
    



def handler():
    try:
        data = updateFunc()
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def handlerLocal():
    try:
        data = updateFuncLocal()
        print(json.dumps(data, indent=4))
    except Exception as e:
        print("message", str(e))

if __name__ == "__main__":
    handlerLocal()