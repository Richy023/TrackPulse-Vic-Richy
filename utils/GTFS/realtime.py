import os

from dotenv import load_dotenv
import requests

load_dotenv()

def getVehiclePositions(mode):
    headers = {"KeyID": os.getenv('TRANSPORT_VIC_API_KEY')}
    if mode == 'vline':
        url = "https://api.opendata.transport.vic.gov.au/opendata/public-transport/gtfs/realtime/v1/vline/vehicle-positions?format=json"
    if mode == 'metro':
        url = 'https://api.opendata.transport.vic.gov.au/opendata/public-transport/gtfs/realtime/v1/metro/vehicle-positions?format=json'

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise RuntimeError(f"HTTP {resp.status_code} when fetching GTFS data")
    return resp.json()

