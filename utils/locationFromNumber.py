from utils.checktype import trainType
from utils.search import *
import json
import folium
from folium import plugins
from io import BytesIO
from PIL import Image
import threading
import asyncio
from staticmap import StaticMap, CircleMarker, IconMarker, Line
import os

from utils.trainImage import getIcon

routes = [
    {"route_id": 1, "route_name": "Alamein"},
    {"route_id": 2, "route_name": "Belgrave"},
    {"route_id": 3, "route_name": "Craigieburn"},
    {"route_id": 4, "route_name": "Cranbourne"},
    {"route_id": 5, "route_name": "Mernda"},
    {"route_id": 6, "route_name": "Frankston"},
    {"route_id": 7, "route_name": "Glen Waverley"},
    {"route_id": 8, "route_name": "Hurstbridge"},
    {"route_id": 9, "route_name": "Lilydale"},
    {"route_id": 11, "route_name": "Pakenham"},
    {"route_id": 12, "route_name": "Sandringham"},
    {"route_id": 13, "route_name": "Stony Point"},
    {"route_id": 14, "route_name": "Sunbury"},
    {"route_id": 15, "route_name": "Upfield"},
    {"route_id": 16, "route_name": "Werribee"},
    {"route_id": 17, "route_name": "Williamstown"},
    {"route_id": 1482, "route_name": "Showgrounds - Flemington Racecourse"}
]

def find_vehicle_by_descriptor_id(data, search_string):
        results = []
        parts = search_string.split('-')
        
        for run in data.get("runs", []):
            if run.get("vehicle_descriptor") and all(part in run["vehicle_descriptor"]["id"] for part in parts):
                result = {
                    "vehicle_position": run["vehicle_position"],
                    "run_ref": run["run_ref"],  # Include run_ref in the result
                    "route_id": run["route_id"]
                }
                results.append(result)
        print(f' RESILSTS THING: {results}')
        return results

def getTrainLocation(Tnumber):

    def process_route(route):
        json_data = runs_api_request(route["route_id"])
        results = find_vehicle_by_descriptor_id(json_data, Tnumber)
        if results:
            all_results.extend(results)
    
    all_results = []
    threads = []
    
    for route in routes:
        thread = threading.Thread(target=process_route, args=(route,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return all_results


tramRoutes = [
    {"route_id": 721, "route_name": "1"},
    {"route_id": 722, "route_name": "109"},
    {"route_id": 724, "route_name": "16"},
    {"route_id": 725, "route_name": "19"},
    {"route_id": 887, "route_name": "57"},
    {"route_id": 897, "route_name": "59"},
    {"route_id": 909, "route_name": "64"},
    {"route_id": 913, "route_name": "67"},
    {"route_id": 940, "route_name": "70"},
    {"route_id": 947, "route_name": "72"},
    {"route_id": 958, "route_name": "75"},
    {"route_id": 976, "route_name": "78"},
    {"route_id": 1002, "route_name": "82"},
    {"route_id": 1041, "route_name": "96"},
    {"route_id": 1083, "route_name": "5"},
    {"route_id": 1880, "route_name": "30"},
    {"route_id": 1881, "route_name": "86"},
    {"route_id": 2903, "route_name": "48"},
    {"route_id": 3343, "route_name": "11"},
    {"route_id": 8314, "route_name": "12"},
    {"route_id": 11529, "route_name": "58"},
    {"route_id": 11544, "route_name": "6"},
    {"route_id": 15833, "route_name": "3"},
    {"route_id": 15834, "route_name": "35"},
]

def getTramLocation(Tnumber):

    def process_route(route):
        json_data = runs_api_request(route["route_id"])
        results = find_vehicle_by_descriptor_id(json_data, Tnumber)
        if results:
            all_results.extend(results)
    
    all_results = []
    threads = []
    
    for route in tramRoutes:
        thread = threading.Thread(target=process_route, args=(route,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return all_results

def getGeopath(runId):
    data = runs_ref_api_request(runId)
    json_data = data
    coordinates = []
    # Ensure 'geopath' exists in the JSON response
    if 'geopath' in json_data['runs'][0]:
        geopath = json_data['runs'][0]['geopath']
        
        # Iterate over each path
        for path in geopath:
            paths = path['paths']
            return paths
    else:
        print("No 'geopath' found in JSON data.")
        return None
    
def generate_google_maps_link(latitude, longitude):
        base_url = "https://www.google.com/maps/search/?api=1&query="
        coordinates = f"{latitude},{longitude}"
        return base_url + coordinates

def convertTrainLocationToGoogle(data):
    
    
    for item in data:
        latitude = item['vehicle_position']['latitude']
        longitude = item['vehicle_position']['longitude']
        google_maps_link = generate_google_maps_link(latitude, longitude)
        return google_maps_link
    
async def makeMapv2(lat, long, name, geopath):
    config = dotenv_values(".env")
    key = config['THUNDERFOREST_MAP']

    def create_map_and_save():
        # Coordinates for the pin
        latitude = lat # + 0.00045
        longitude = long
        print('started map gen')
        
        # Create a static map centered at the coordinates with the desired zoom level
        # m = StaticMap(1024, 1024, 12, url_template='https://tile.thunderforest.com/transport/{z}/{x}/{y}.png?apikey='+key)
        m = StaticMap(1024, 1024, 12)
        m.set_tile_provider(tile_provider= 'openstreetmap')
        print('created base map')
        
        # Split the coordinates into individual pairs
        # pairs = str(geopath[0].replace(',','')).split(" ")
        # print(f'MONOR: {pairs}')

        # for i in range(0, len(pairs)-2, 2):
        #     lat1 = float(pairs[i])
        #     lon1 = float(pairs[i+1])
        #     lat2 = float(pairs[i+2])
        #     lon2 = float(pairs[i+3])
            
        #     line = Line([(lon1, lat1), (lon2, lat2)], 'blue', 3)
        #     m.add_line(line)
            
        # Add a marker at the coordinates
        icon_train = IconMarker((longitude, latitude), './utils/metro.png', 25, 25)  # Adjusted to use latitude and longitude correctly
        # marker = CircleMarker((longitude, latitude), '#008dd0', 20)

        m.add_marker(icon_train)
        # m.add_marker(marker)
        print('added marker')

        # Render the map
        image = m.render(zoom=14)

        # Save the map as a  PNG file
        image.save(f'temp/{name}-map.png')
        print('saved map')
        
        # Run create_map_and_save in a separate thread
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, create_map_and_save)
    
async def makeMap(point_latitude, point_longitude, name):
    def create_map_and_save():
        try:
            # Get icon URL based on train type
            icon_url = 'https://xm9g.xyz/discord-bot-assets/metro.png'
            print(f'ICON URL: {icon_url}')
            icon = folium.CustomIcon(
                icon_url,
                icon_size=(50, 50),
            )        

            # Create a map centered around the point of interest
            map = folium.Map(location=[point_latitude, point_longitude], zoom_start=15, control_scale=False,)
            
            # Add a marker for the point of interest with custom icon
            folium.Marker([point_latitude, point_longitude], icon=icon, popup=name,).add_to(map)
            
            # Convert the map to PNG image
            print('starting png conversion')
            img_data = map._to_png()
            print('png conversion done')
            
            # Save the image to a file (optional)
            with open(f'temp/{name}-map.png', 'wb') as f:
                f.write(img_data)
            
            # Convert image data to PIL Image
            image = Image.open(BytesIO(img_data))
            
            # Crop image to square
            width, height = image.size
            size = min(width, height)
            left = (width - size) // 2
            top = (height - size) // 2
            right = (width + size) // 2
            bottom = (height + size) // 2
            image = image.crop((left, top, right, bottom))
            
            # Save the cropped image to a file (optional)
            image.save(f'temp/{name}-map.png')
            
        except Exception as e:
            print(f'Error creating map: {e}')

    # Run create_map_and_save in a separate thread
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, create_map_and_save)

