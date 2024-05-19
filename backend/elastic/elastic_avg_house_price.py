from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

JSON_INDENT = 4
INDEX_NAME = 'avg_house_price'

client = Elasticsearch(
    "https://localhost:9200",
    verify_certs=False,
    basic_auth=("elastic", os.getenv("ES_PASSWORD"))
)

def insert_avg_house_price_data():
    # Load the JSON file
    with open('./../../database/avg_house_price.json', 'r') as file:
        avg_house_price_data = json.load(file)

    for index, avg_house_price in enumerate(avg_house_price_data):
        avg_house_price['_index'] = INDEX_NAME

    response = bulk(client, avg_house_price_data)
    return response

# test the connection
print(client.info())
print(insert_avg_house_price_data())