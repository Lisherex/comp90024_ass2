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
    verify_certs=False,
    basic_auth=("elastic", os.getenv("ELASTIC_PASSWORD"))
)


def insert_copd_data():
    # Load the JSON file
    with open('./../../database/copdFinalData.json', 'r') as file:
        copd_data = json.load(file)

    for index, copd in enumerate(copd_data):
        copd['_index'] = INDEX_NAME

    response = bulk(client, copd_data)
    return response

# test the connection
print(client.info())
print(insert_copd_data())