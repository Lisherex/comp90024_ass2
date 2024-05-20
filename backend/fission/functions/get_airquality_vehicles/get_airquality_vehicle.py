from elasticsearch import Elasticsearch, helpers
import json
import os
import logging
from collections import defaultdict
from config import Config

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def fetch_vehicle_data(client):
    res = client.search(
        index='vehicle*',
        body={
            'size': 10000,
            'query': {
                'match_all': {}
            },
        }
    )
    return res['hits']['hits']

def fetch_air_quality_data(client):
    res = client.search(
        index='airquality*',
        body={
            'size': 10000,
            'query': {
                'match_all': {}
            }
        }
    )
    return res['hits']['hits']


def merge_data(air_quality_hits, vehicle_hits):
    merged_data = []

    for hit in air_quality_hits:
        site_id = hit['_source']['site_id']
        site_name = hit['_source']['site_name']
        site_location = hit['_source']['site_location']
        value = hit['_source']['value']
        unit = hit['_source']['unit']
        health_advice = hit['_source']['health_advice']
        health_advice_color = hit['_source']['health_advice_color']

        matching_vehicle_hit = None

        for vehicle_hit in vehicle_hits:
            if vehicle_hit['_source']['station_id'] == site_id:
                matching_vehicle_hit = vehicle_hit
                break

        if matching_vehicle_hit:
            vehicles = matching_vehicle_hit['_source']
            merged_data.append({
                "site_id": site_id,
                "site_name": site_name,
                "site_location" : site_location,
                "value": value,
                "unit": unit,
                "health_advice": health_advice,
                "health_advice_color": health_advice_color,
                "lga_name": vehicles['lga_name'],
                "lga_code": vehicles['lga_code'],
                "none_vehicle_per_dwelling": vehicles['none_vehicle_per_dwelling'],
                "one_vehicle_per_dwelling": vehicles['one_vehicle_per_dwelling'],
                "two_vehicle_per_dwelling": vehicles['two_vehicle_per_dwelling'],
                "three_vehicle_per_dwelling": vehicles['three_vehicle_per_dwelling'],
                "more_than_four_vehicle_per_dwelling": vehicles['more_than_four_vehicle_per_dwelling'],
                "total_dwelling": vehicles['total_dwelling']
            })

    return merged_data

def main():
    configLoader = Config(True)
    secretLoader = Config(False)

    url = configLoader("internal-service-ports", "ELASTIC_SEARCH_URL")
    port = configLoader("internal-service-ports", "ELASTIC_SEARCH_PORT")
    username = secretLoader("auth", "ES_USERNAME")
    password = secretLoader("auth", "ES_PASSWORD")

    try:
        client = Elasticsearch(
            f'{url}:{port}',
            verify_certs=False,
            basic_auth=(username, password)
        )

        # Fetch data
        vehicle_hits = fetch_vehicle_data(client)
        air_quality_hits = fetch_air_quality_data(client)
        #return json.dumps(air_quality_hits, indent=4)

        # Merge data
        merged_results = merge_data(air_quality_hits, vehicle_hits)

        return json.dumps(merged_results, indent=4)

    except Exception as e:
        logger.error(f"Error connecting to Elasticsearch: {e}")

# if __name__ == "__main__":
#     data = main()
#     print(data)
