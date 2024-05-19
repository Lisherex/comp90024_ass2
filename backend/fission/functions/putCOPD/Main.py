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

def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            return None  # or return date_str if you want to keep the original on error

def find_admissions(data, lga_code, key):
    for item in data:
        if item['properties']['lga_code'] == lga_code:
            return item['properties'].get(key, None)
    return None



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
                # Load data from JSON files
                with open('./sudo/PHIDU_-_Admissions_-_Principal_Diagnosis__Persons___LGA__2017-2018.json/phidu_admiss_principal_diag_persons_lga_2017_18-7740618646483850644.json', 'r') as file:
                    persons_data = json.load(file)['features']

                with open('./sudo/PHIDU_-_Admissions_-_Principal_Diagnosis__Males___LGA__2017-2018.json/phidu_admiss_principal_diag_males_lga_2017_18-130600776371740895.json', 'r') as file:
                    males_data = json.load(file)['features']

                with open('./sudo/PHIDU_-_Admissions_-_Principal_Diagnosis__Females___LGA__2017-2018.json/phidu_admiss_principal_diag_females_lga_2017_18-4964261224904708593.json', 'r') as file:
                    females_data = json.load(file)['features']

                with open('./climateStation/all_sites.json', 'r') as file:
                    sites_data = json.load(file)['records']

                # Initialize the geolocator
                geolocator = Nominatim(user_agent="UniqueAppNameForProject")
                results = []

                for i, lga in enumerate(persons_data):
                    lga_properties = lga['properties']
                    lga_code = lga_properties['lga_code']
                    lga_name = lga_properties['lga_name']
                    try:
                        location = geolocator.geocode(f"{lga_name}, Victoria, Australia", timeout=10)
                    except Exception as e:
                        print(f"Geolocation API error for {lga_name}: {e}")
                        location = None

                    closest_site_id = "Location not found"  # Default if geolocation fails
                    if location:
                        min_distance = float('inf')
                        for site in sites_data:
                            site_coords = site['geometry']['coordinates']
                            distance = haversine(location.latitude, location.longitude, site_coords[0], site_coords[1])
                            if distance < min_distance:
                                min_distance = distance
                                closest_site_id = site['siteID']

                    result = {
                        "id": i,
                        "lga_code": lga_code,
                        "lga_name": lga_name,
                        "station_id": closest_site_id,
                        "admissions_respiratory_system_diseases_public_hospital_total_number": find_admissions(persons_data, lga_code, 'admssns_rsprtry_systm_dsss_prsns_pblc_hsptls_201718_nmbr'),
                        "admissions_respiratory_system_diseases_public_hospital_males_number": find_admissions(males_data, lga_code, 'admssns_rsprtry_systm_dsss_mls_pblc_hsptls_201718_nmbr'),
                        "admissions_respiratory_system_diseases_public_hospital_females_number": find_admissions(females_data, lga_code, 'admssns_rsprtry_systm_dsss_fmls_pblc_hsptls_201718_nmbr'),
                        "admissions_chronic_obstructive_pulmonary_disease_public_hospital_total_number": find_admissions(persons_data, lga_code, 'admsn_chrn_obstrcve_plmnry_dse_cpd_prsn_pblc_hsptl_201718_nmbr'),
                        "admissions_chronic_obstructive_pulmonary_disease_public_hospital_males_number": find_admissions(males_data, lga_code, 'admsn_chrn_obstrcve_plmnry_dse_cpd_mls_pblc_hsptl_201718_nmbr'),
                        "admissions_chronic_obstructive_pulmonary_disease_public_hospital_females_number": find_admissions(females_data, lga_code, 'admsn_chrn_obstrcve_plmnry_dse_cpd_fmls_pblc_hsptl_201718_nmbr'),
                    }
                    results.append(result)
            return results
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