from Config import Config
from elasticsearch import Elasticsearch, helpers

def main():
    configLoader = Config(True)
    secretLoader = Config(False)



    url = configLoader("internal-service-ports", "ELASTIC_SEARCH_URL")
    port = configLoader("internal-service-ports", "ELASTIC_SEARCH_PORT")
    username = secretLoader("auth", "ES_USERNAME")
    password = secretLoader("auth", "ES_PASSWORD")
    es = Elasticsearch(f"{url}:{port}",
                       verify_certs=False,
                       basic_auth=(username, password)
                       )
    del url, port, username, password

    
    pass