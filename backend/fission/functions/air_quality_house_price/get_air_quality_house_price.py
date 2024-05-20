import json
from elasticsearch import Elasticsearch

def main():
    # configLoader = Config(True)
    # secretLoader = Config(False)
    #
    # url = configLoader("internal-service-ports", "ELASTIC_SEARCH_URL")
    # port = configLoader("internal-service-ports", "ELASTIC_SEARCH_PORT")
    # username = secretLoader("auth", "ES_USERNAME")
    # password = secretLoader("auth", "ES_PASSWORD")
    #
    # client = Elasticsearch(
    #     f'{url}:{port}',
    #     verify_certs=False,
    #     basic_auth=(username, password)
    # )

    client = Elasticsearch(
        'https://localhost:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )

    # Initialize a scroll session for air quality data
    air_quality_data = client.search(
        index='airquality',
        body={
            'size': 1000,
            'query': {
                'match_all': {}
            }
        },
        scroll='1m'  # Scroll for large datasets
    )

    air_quality_scroll_id = air_quality_data['_scroll_id']
    response = []

    # Process each document in air quality data
    while True:
        for doc in air_quality_data['hits']['hits']:
            source = doc['_source']
            site_id = source.get('site_id')
            site_name = source.get('site_name')
            lat = source.get('site_location', {}).get('lat')
            lon = source.get('site_location', {}).get('lon')
            value = source.get('value')
            unit = source.get('unit')
            health_advice = source.get('health_advice')
            health_advice_color = source.get('health_advice_color')

            # Fetch the average house price for the site_id
            house_price_data = client.search(
                index='avg_house_price',
                body={
                    'query': {
                        'match': {'station_id': site_id}
                    }
                }
            )
            average_price = None
            if house_price_data['hits']['hits']:
                average_price = house_price_data['hits']['hits'][0]['_source']['average_price']

            response.append({
                'site_id': site_id,
                'site_name': site_name,
                'site_location': {
                    'latitude': lat,
                    'longitude': lon
                },
                'value': value,
                'unit': unit,
                'health_advice': health_advice,
                'health_advice_color': health_advice_color,
                'average_price': average_price  # Include average house price in the output
            })

        air_quality_data = client.scroll(scroll_id=air_quality_scroll_id, scroll='1m')
        if len(air_quality_data['hits']['hits']) == 0:
            break

    client.clear_scroll(scroll_id=air_quality_scroll_id)

    # Return the results as a formatted JSON string
    return json.dumps(response, indent=4)

if __name__ == '__main__':
    data = main()
    print(data)