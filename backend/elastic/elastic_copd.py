from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

JSON_INDENT = 4
INDEX_NAME = 'copd'

client = Elasticsearch(
    "https://localhost:9200",
    varify_certs=False,
    basic_auth=("elastic", os.getenv("ELASTIC_PASSWORD"))
)


def insert_copd_data():
    copd_data = []
    # Load the JSON file
    with open('./../../database/sudo/PHIDU_-_Admissions_-_Principal_Diagnosis__Females___LGA__2017-2018.json/phidu_admiss_principal_diag_females_lga_2017_18-4964261224904708593.json', 'r') as file:
        data = json.load(file)

    for feature in data['features']:
        copd = {}
        copd['admissions_respiratory_system_diseases_per_100000_females'] = feature['properties']['admssns_rsprtry_systm_dsss_fmls_hsptls_201718_asr_pr_100000']
        copd['lga_name'] = feature['properties']['lga_name']
        copd['lga_code'] = feature['properties']['lga_code']

        copd_data.append(copd)

    response = bulk(client, copd_data)
    return response
