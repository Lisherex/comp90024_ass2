import urllib.request
import urllib.parse
import json

class EnvironmentMonitorAPI:
    def __init__(self, hdr: dict, baseURL) -> None:
        # self.hdr = hdr
        # self.baseURL = baseURL
        pass

    @staticmethod
    def constructURL(baseURL, params: dict) -> str:
        queryString = urllib.parse.urlencode(params)

        return f"{baseURL}?{queryString}"
    
    @staticmethod
    def getSiteData(baseURL:str, params:dict, hdr:dict) -> dict:

        url = f"{baseURL}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers=hdr)

        try:
            with urllib.request.urlopen(req) as response:
                resBody = response.read().decode("utf-8")
                data = json.loads(resBody)
                return data
        except urllib.error.HTTPError as e:
            print(f"HTTP error occurred: {e.code} {e.reason}")
        except urllib.error.URLError as e:
            print(f"URL error occurred: {e.reason}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return {}
