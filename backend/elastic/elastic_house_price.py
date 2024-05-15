from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

JSON_INDENT = 4
INDEX_NAME = 'houseprice'

client = Elasticsearch(
    "https://localhost:9200",
    verify_certs=False,
    basic_auth=("elastic", os.getenv("ELASTIC_PASSWORD"))
)


def insert_house_price_data():
    # Load the JSON file
    with open('./../../database/housePriceFinalData.json', 'r') as file:
        house_price_data = json.load(file)

    for index, house_price in enumerate(house_price_data):
        house_price['_index'] = INDEX_NAME

    response = bulk(client, house_price_data)
    return response

# test the connection
print(client.info())
print(insert_house_price_data())