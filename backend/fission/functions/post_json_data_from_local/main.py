from flask import request, jsonify, current_app
from elasticsearch import Elasticsearch, helpers
import json
import logging
from config import Config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    index_name = request.headers["X-Fission-Params-index"]
    if not index_name:
        current_app.logger.error("Index name not provided/Invalid Index")
        return jsonify({"error": "Index name not provided/Invalid Index"}), 400
    
    configLoader = Config(True)
    secretLoader = Config(False)

    url = configLoader("internal-service-ports", "ELASTIC_SEARCH_URL")
    port = configLoader("internal-service-ports", "ELASTIC_SEARCH_PORT")
    username = secretLoader("auth", "ES_USERNAME")
    password = secretLoader("auth", "ES_PASSWORD")
    
    try:
        client = Elasticsearch(
            f'{url}:{port}',
            verify_certs=False,
            basic_auth=(username, password)
        )
    except Exception as e:
        logger.error(f"Error connecting to Elasticsearch: {e}")
    
    data = request.get_json()

    if not data:
        current_app.logger.error("No data provided")
        return jsonify({"error": "No data provided"}), 400

    actions = []
    for entry in data:
        entry["_index"] = index_name
        actions.append(entry)

    try:
        helpers.bulk(client, actions)
        current_app.logger.info("Successfully upload Data")
        return jsonify({"message": "Successfully upload Data"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    