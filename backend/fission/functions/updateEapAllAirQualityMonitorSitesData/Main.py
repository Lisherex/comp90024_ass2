import os
import json
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers
import urllib.request
import urllib.parse
import json
from Config import Config

load_dotenv()

ALL_AIR_MONITORING_SITES_URL = os.getenv('ALL_AIR_MONITORING_SITES_URL')
ELASTIC_SEARCH_URL = os.getenv('ELASTIC_SEARCH_URL')
ELASTIC_SEARCH_PORT = os.getenv('ELASTIC_SEARCH_PORT')
ES_USERNAME = os.getenv('ES_USERNAME')
ES_PASSWORD = os.getenv('ES_PASSWORDc')
EPA_APIKEY = os.getenv('EPA_APIKEY')

class EnvironmentMonitorAPI:
    # def __init__(self, hdr: dict, baseURL) -> None:
    def __init__(self) -> None:
        # self.hdr = hdr
        # self.baseURL = baseURL
        pass

    @staticmethod
    def constructURL(baseURL, params: dict) -> str:
        queryString = urllib.parse.urlencode(params)

        return f"{baseURL}?{queryString}"

    @staticmethod
    def getSiteData(baseURL: str, params: dict, hdr: dict) -> dict:
        url = f"{baseURL}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers=hdr)

        try:
            with urllib.request.urlopen(req) as response:
                resBody = response.read().decode("utf-8")
                data = json.loads(resBody)
                return data
        except urllib.error.HTTPError as e:
            print(f"HTTP error occurred: {e.code} {e.reason}")
            raise
        except urllib.error.URLError as e:
            print(f"URL error occurred: {e.reason}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

def updateFunc():
    configLoader = Config(True)
    secretLoader = Config(False)

    try:
        data = EnvironmentMonitorAPI.getSiteData(
            baseURL=configLoader("api-urls", "ALL_AIR_MONITORING_SITES_URL"),
            params={"environmentalSegment": "air"},
            hdr={
                "Cache-Control": "no-cache",
                "X-API-Key": secretLoader("auth", "EPA_APIKEY"),
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            }
        )
    except urllib.error.HTTPError as e:
        print(f"Handled HTTP error: {e.code} {e.reason}")
        raise
    except urllib.error.URLError as e:
        print(f"Handled URL error: {e.reason}")
        raise
    except Exception as e:
        print(f"Handled unexpected error: {e}")
        raise

    return data


    # url = configLoader("internal-service-ports", "ELASTIC_SEARCH_URL")
    # port = configLoader("internal-service-ports", "ELASTIC_SEARCH_PORT")
    # username = secretLoader("auth", "ES_USERNAME")
    # password = secretLoader("auth", "ES_PASSWORD")
    # es = Elasticsearch(f"{url}:{port}",
    #                    verify_certs=False,
    #                    basic_auth=(username, password)
    #                    )
    # del url, port, username, password
    # # info = es.info().body
    # # return info

    # actions = []
    # for record in data.get("records", []):
    #     site_id = record.get("siteID")
    #     site_name = record.get("siteName")
    #     coordinates = record.get("geometry", {}).get("coordinates")
    #     if not coordinates:
    #         continue

    #     for advice in record.get("siteHealthAdvices", []):
    #         document_id = f"{site_id}_{advice.get("since")}"
    #         action = {
    #             "_index": "airquality",
    #             "_id": document_id,
    #             "_source": {
    #                 "siteId": site_id,
    #                 "siteName": site_name,
    #                 "siteLocation": {"lat": coordinates[0], "lon": coordinates[1]},
    #                 "parameter": advice.get("healthParameter"),
    #                 "value": advice.get("averageValue"),
    #                 "unit": advice.get("unit"),
    #                 "healthAdvice": advice.get("healthAdvice"),
    #                 "healthAdviceColor": advice.get("healthAdviceColor"),
    #                 "since": advice.get("since"),
    #                 "until": advice.get("until"),
    #             }
    #         }
    #         actions.append(action)

    # if actions:
    #     response = helpers.bulk(es, actions)

    # return response

def updateFuncLocal():

    try:
        data = EnvironmentMonitorAPI.getSiteData(
            baseURL=ALL_AIR_MONITORING_SITES_URL,
            params={"environmentalSegment": "air"},
            hdr={
                "Cache-Control": "no-cache",
                "X-API-Key":EPA_APIKEY,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            }
        )
    except urllib.error.HTTPError as e:
        print(f"Handled HTTP error: {e.code} {e.reason}")
        raise
    except urllib.error.URLError as e:
        print(f"Handled URL error: {e.reason}")
        raise
    except Exception as e:
        print(f"Handled unexpected error: {e}")
        raise

    # return data


    url = ELASTIC_SEARCH_URL
    port = ELASTIC_SEARCH_PORT
    username = ES_USERNAME
    password = ES_PASSWORD
    es = Elasticsearch(f"{url}:{port}",
                       verify_certs=False,
                       basic_auth=(username, password)
                       )
    del url, port, username, password
    # info = es.info().body
    # return info

    actions = []
    for record in data.get("records", []):
        site_id = record.get("siteID")
        site_name = record.get("siteName")
        coordinates = record.get("geometry", {}).get("coordinates")
        if not coordinates:
            continue
        
        for advice in record.get("siteHealthAdvices", []):
            document_id = f"{site_id}_{advice.get('since')}"
            action = {
                "_index": "airquality",
                "_id": document_id,
                "_source": {
                    "site_id": site_id,
                    "site_name": site_name,
                    "site_location": {"lat": coordinates[0], "lon": coordinates[1]},
                    "parameter": advice.get("healthParameter"),
                    "value": advice.get("averageValue"),
                    "unit": advice.get("unit"),
                    "health_advice": advice.get("healthAdvice"),
                    "health_advice_color": advice.get("healthAdviceColor"),
                    "since": advice.get("since"),
                    "until": advice.get("until"),
                }
            }
            actions.append(action)

    # return actions
    
    if actions:
        response = helpers.bulk(es, actions)
        return response


def handler():
    try:
        data = updateFunc()
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def handlerLocal():
    try:
        data = updateFuncLocal()
        print(json.dumps(data, indent=4))
    except Exception as e:
        print("message", str(e))

if __name__ == "__main__":
    handlerLocal()