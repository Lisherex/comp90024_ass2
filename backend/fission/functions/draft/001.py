import requests

def main():
    url = "https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites"
    headers = {
        "Cache-Control": "no-cache",
        "X-API-Key": "7d3c9901e475402f844691c300e4efa8",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    params = {
        "environmentalSegment": "air",
        "location":"[-37.78, 145.023]"
    }

    response = requests.get(url, headers=headers, params=params)

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    return None

if __name__ == "__main__":
    main()

