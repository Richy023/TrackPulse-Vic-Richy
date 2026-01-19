import requests
from google.transit import gtfs_realtime_pb2
from dotenv import *

config = dotenv_values(".env")
TRANSPORT_VIC_API_KEY = config['TRANSPORT_VIC_API_KEY']

def tramtracker(plate):
    stops = []
    # GTFS-R endpoint for trams
    url = "https://api.opendata.transport.vic.gov.au/opendata/public-transport/gtfs/realtime/v1/tram/vehicle-positions"
    headers = {
        "KeyId": TRANSPORT_VIC_API_KEY
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        with open("recentsave.txt", "w") as file:
            file.write(str(feed.entity))
        for entity in feed.entity:
            if entity.HasField("vehicle"):
                vehicle = entity.vehicle
                busplate = vehicle.vehicle.id
                route_id = vehicle.trip.route_id
                trip_id = vehicle.trip.trip_id
                if busplate == plate:
                    location = f"{vehicle.position.latitude},{vehicle.position.longitude}"
                    stops.append({
                        "trip_id": trip_id,
                        "location": location,
                        "route_id": route_id,
                    })
        return stops
                    
    else:
        print(f"Error: {response.status_code}")