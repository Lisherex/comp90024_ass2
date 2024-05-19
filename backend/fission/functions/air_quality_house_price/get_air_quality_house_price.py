import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

def main():
    client = Elasticsearch(
        'https://localhost:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )

    # Initialize a scroll session for air quality data
    air_quality_data = scan(
        client=client,
        index='airquality*',
        query={
            'query': {
                'match_all': {}
            }
        },
        size=1000  # Retrieves 1000 docs at a time
    )

    response = []

    # Process each document in air quality data
    for air_quality in air_quality_data:
        site_id = air_quality['_source']['site_id']

        # Prepare a query to fetch house price data related to the current site_id
        house_price_query = {
            'query': {
                'match': {
                    'station_id': site_id
                }
            }
        }

        # Use the scan helper to fetch house price data related to the current site_id
        house_price_data = scan(
            client=client,
            index='houseprice*',
            query=house_price_query,
            size=1000  # Retrieves 1000 docs at a time
        )

        # Collect house price documents
        documents = [doc['_source'] for doc in house_price_data]
        if documents:
            response.append({
                site_id: documents
            })

    # Return the results as a formatted JSON string
    return json.dumps(response, indent=4)

if __name__ == '__main__':
    data = main()
    print(data)
