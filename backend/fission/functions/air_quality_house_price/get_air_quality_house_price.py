import logging, json
from flask import current_app, request
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

def main():
    client = Elasticsearch(
        # 'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        'https://localhost:9200',
        verify_certs= False,
        basic_auth=('elastic', 'elastic')
    )

    res = client.search(
        index='airquality*',
        body={
            'size': 10000,
            'query': {
                'match_all': {}
            }
        }
    )

    air_quality_data = res['hits']['hits']
    air_quality_site_ids = [air_quality['_source']['site_id'] for air_quality in air_quality_data]
    response = []

    for site_id in air_quality_site_ids:
        doc = {
            'query': {
                'match': {
                    'station_id': site_id
                }
                # 'match_all': {}
            }
        }

        # Use the scan helper to iterate over all documents, size is the batch size
        house_price_data = scan(client=client, index='houseprice*', query=doc, size=1000)

        # Iterate over the results
        documents = []
        for doc in house_price_data:
            documents.append(doc["_source"])
            if len(documents) > 0:
                response.append({
                    site_id: documents
                })

    return json.dumps(response, indent=4)

if __name__ == '__main__':
    data = main()
    print(data, len(data))