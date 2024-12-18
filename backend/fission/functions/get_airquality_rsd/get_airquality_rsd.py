from elasticsearch import Elasticsearch, helpers
import json
import os
# from dotenv import load_dotenv
import logging
from collections import defaultdict
from config import Config

# load_dotenv()

# ELASTIC_SEARCH_URL = os.getenv('ELASTIC_SEARCH_URL')
# ELASTIC_SEARCH_PORT = os.getenv('ELASTIC_SEARCH_PORT')
# ES_USERNAME = os.getenv('ES_USERNAME')
# ES_PASSWORD = os.getenv('ES_PASSWORD')

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def calculate_average_respiratory_admissions(copd_hits):
    admissions_data = defaultdict(lambda: defaultdict(list))

    # Aggregate admissions data by station_id and category
    for hit in copd_hits:
        station_id = hit['_source']['station_id']
        admissions_data[station_id]['total'].append(hit['_source'].get('admissions_respiratory_system_diseases_public_hospital_total_number', 0))
        admissions_data[station_id]['males'].append(hit['_source'].get('admissions_respiratory_system_diseases_public_hospital_males_number', 0))
        admissions_data[station_id]['females'].append(hit['_source'].get('admissions_respiratory_system_diseases_public_hospital_females_number', 0))

    # Calculate average admissions for each category and station_id
    average_admissions = {}
    for station_id, categories in admissions_data.items():
        average_admissions[station_id] = {
            'average_rsd_total': sum(categories['total']) / len(categories['total']),
            'average_rsd_males': sum(categories['males']) / len(categories['males']),
            'average_rsd_females': sum(categories['females']) / len(categories['females'])
        }

    return average_admissions

def fetch_copd_data_all(client):
    res = client.search(
        index='copd*',
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

def merge_data(air_quality_hits, average_respiratory_admissions):
    merged_data = []

    for hit in air_quality_hits:
        site_id = hit['_source']['site_id']
        if site_id in average_respiratory_admissions:
            averages = average_respiratory_admissions[site_id]
            merged_data.append({
                "site_id": site_id,
                "site_name": hit['_source']['site_name'],
                "site_location": hit['_source']['site_location'],
                "value": hit['_source']['value'],
                "unit": hit['_source']['unit'],
                "health_advice": hit['_source']['health_advice'],
                "health_advice_color": hit['_source']['health_advice_color'],
                "average_total_rsd_admissions_num": averages['average_rsd_total'],
                "average_male_rsd_admissions_num": averages['average_rsd_males'],
                "average_female_rsd_admissions_num": averages['average_rsd_females']
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
        # client = Elasticsearch(
        #     f'{ELASTIC_SEARCH_URL}:{ELASTIC_SEARCH_PORT}',
        #     verify_certs=False,
        #     basic_auth=(ES_USERNAME, ES_PASSWORD)
        # )
        client = Elasticsearch(f'{url}:{port}',
                                verify_certs=False,
                                basic_auth=(username, password)
                                )

        # Fetch data
        copd_hits_all = fetch_copd_data_all(client)
        air_quality_hits = fetch_air_quality_data(client)

        # Calculate average respiratory admissions
        average_respiratory_admissions = calculate_average_respiratory_admissions(copd_hits_all)

        # Merge data
        merged_results = merge_data(air_quality_hits, average_respiratory_admissions)
        # print("merged_results: ", json.dumps(merged_results, indent=4))
        return json.dumps(merged_results, indent=4)


    except Exception as e:
        logger.error(f"Error connecting to Elasticsearch: {e}")

# if __name__ == "__main__":
#     main()
