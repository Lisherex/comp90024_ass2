from elasticsearch import Elasticsearch, helpers
import json
import os
import logging
from collections import defaultdict
from Config import Config

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# def calculate_average_copd_admissions(copd_hits):
#     admissions_data = defaultdict(lambda: defaultdict(list))

    

#     for hit in copd_hits:
#         station_id = hit['_source']['station_id']
#         # Replace None with 0 using the `or 0` pattern
#         total = hit['_source'].get('admissions_chronic_obstructive_pulmonary_disease_public_hospital_total_number', 0) or 0
#         males = hit['_source'].get('admissions_chronic_obstructive_pulmonary_disease_public_hospital_males_number', 0) or 0
#         females = hit['_source'].get('admissions_chronic_obstructive_pulmonary_disease_public_hospital_females_number', 0) or 0

#         admissions_data[station_id]['total'].append(total)
#         admissions_data[station_id]['males'].append(males)
#         admissions_data[station_id]['females'].append(females)

#     average_admissions = {}
#     for station_id, categories in admissions_data.items():
#         total_count = len(categories['total'])
#         male_count = len(categories['males'])
#         female_count = len(categories['females'])

#         average_admissions[station_id] = {
#             'average_copd_total': sum(categories['total']) / total_count if total_count else 0,
#             'average_copd_males': sum(categories['males']) / male_count if male_count else 0,
#             'average_copd_females': sum(categories['females']) / female_count if female_count else 0
#         }

#     return average_admissions
    

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

    # for hit in avg_house_price_hits:
    #     station_id = hit['_source']['station_id']
    #     avg_price = hit['_source']['average_price']
    #     if station_id in vehicle_hits['_source']:
    #         vehicles = vehicle_hits['_source'][station_id]
    #         merged_data.append({
    #             "station_id": station_id,
    #             "average_price": avg_price,
    #             "lga_name": vehicles['_source']['lga_name'],
    #             "lga_code": vehicles['_source']['lga_code'],
    #             "none_vehicle_per_dwelling": vehicles['_source']['none_vehicle_per_dwelling'],
    #             "one_vehicle_per_dwelling": vehicles['_source']['one_vehicle_per_dwelling'],
    #             "two_vehicle_per_dwelling": vehicles['_source']['two_vehicle_per_dwelling'],
    #             "three_vehicle_per_dwelling": vehicles['_source']['three_vehicle_per_dwelling'],
    #             "more_than_four_vehicle_per_dwelling": vehicles['_source']['more_than_four_vehicle_per_dwelling'],
    #             "total_dwelling": vehicles['_source']['total_dwelling']
    #         })

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
#     main()
