from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

JSON_INDENT = 4
INDEX_NAME = 'vehicle'

client = Elasticsearch(
    "https://localhost:9200",
    verify_certs=False,
    basic_auth=("elastic", os.getenv("ELASTIC_PASSWORD"))
)

def insert_vehicle_data():
    # Load the JSON file
    with open('./../../database/vehicleFinalData.json', 'r') as file:
        vehicle_data = json.load(file)

    for index, vehicle in enumerate(vehicle_data):
        vehicle['_index'] = INDEX_NAME

    response = bulk(client, vehicle_data)
    return response

# test the connection
print(client.info())
print(insert_vehicle_data())