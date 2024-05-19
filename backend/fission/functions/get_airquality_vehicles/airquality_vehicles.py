import os
from elasticsearch import Elasticsearch
import json

def get_data_from_elasticsearch(client, index):
    """Fetch all records from a specific Elasticsearch index."""
    try:
        response = client.search(index=index, body={"query": {"match_all": {}}}, size=1000)
        return [hit["_source"] for hit in response['hits']['hits']]
    except Exception as e:
        print(f"Error fetching data from {index}:", e)
        return []

def main():
    # Configure Elasticsearch connection
    es = Elasticsearch(
        ["https://localhost:9200/"],
        verify_certs=False,
        basic_auth=("elastic", "elastic")
    )

    # Fetch data from airquality index
    air_quality_data = get_data_from_elasticsearch(es, 'airquality')
    # Fetch data from vehicle index
    vehicle_data = get_data_from_elasticsearch(es, 'vehicle')

    # Output the fetched data
    print("Air Quality Data:")
    for data in air_quality_data:
        print(data)

    print("\nVehicle Data:")
    for data in vehicle_data:
        print(data)

if __name__ == "__main__":
    result = main()
    print(result)