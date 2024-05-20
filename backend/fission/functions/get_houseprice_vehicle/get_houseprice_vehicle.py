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

def fetch_avg_house_price_data(client):
    res = client.search(
        index='avg_house_price*',
        body={
            'size': 10000,
            'query': {
                'match_all': {}
            }
        }
    )
    return res['hits']['hits']

def merge_data(avg_house_price_hits, vehicle_hits):
    merged_data = []

    for avg_hit in avg_house_price_hits:
        station_id = avg_hit['_source']['station_id']
        avg_price = avg_hit['_source']['average_price']
        matching_vehicle_hit = None

        for vehicle_hit in vehicle_hits:
            if vehicle_hit['_source']['station_id'] == station_id:
                matching_vehicle_hit = vehicle_hit
                break

        if matching_vehicle_hit:
            vehicles = matching_vehicle_hit['_source']
            merged_data.append({
                "station_id": station_id,
                "average_price": avg_price,
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
        #return json.dumps(vehicle_hits, indent=4)
        avg_house_price_hits = fetch_avg_house_price_data(client)
        #return json.dumps(avg_house_price_hits, indent=4)

        # Merge data
        merged_results = merge_data(avg_house_price_hits, vehicle_hits)

        return json.dumps(merged_results, indent=4)

    except Exception as e:
        logger.error(f"Error connecting to Elasticsearch: {e}")

# if __name__ == "__main__":
#     data = main()
#     print(data)
