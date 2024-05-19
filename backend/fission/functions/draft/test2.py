import urllib.request

url = "https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites?environmentalSegment=air&location=%5B-37.78,%20145.023%5D"
hdr = {
    'Cache-Control': 'no-cache',
    'X-API-Key': '7d3c9901e475402f844691c300e4efa8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

req = urllib.request.Request(url, headers=hdr)

try:
    with urllib.request.urlopen(req) as response:
        print("Status Code:", response.getcode())
        print("Response Headers:", response.info())
        print("Response Body:", response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print("HTTPError:", e.code, e.reason)
except urllib.error.URLError as e:
    print("URLError:", e.reason)
except Exception as e:
    print("Error:", e)
