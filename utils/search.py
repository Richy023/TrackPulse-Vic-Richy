import requests
from utils.keyCalc import *
import csv
import json
import os
import pickle
import time
from pathlib import Path

def search_api_request(search_term):
    url = getUrl(f"/v3/search/{search_term}")
    print(f"Search url: {url}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        formatted = format(data)
        print(formatted)
        return(data)
    else:

        print(f"Error: {response.status_code} - {response.text}")

def route_api_request(route_id, route_type):
    
    url = getUrl(f'/v3/routes/?route_name={route_id}&route_types={route_type}')
    print(f"Route search url: {url}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        formatted = format(data)
        print(formatted)
        return(formatted)
    else:

        print(f"Error: {response.status_code} - {response.text}")

def route_api_request_id(route_id):
    
    url = getUrl(f'/v3/routes/?route_id={route_id}')
    print(f"Route search url: {url}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        formatted = format(data)
        print(formatted)
        return(formatted)
    else:

        print(f"Error: {response.status_code} - {response.text}")
        
def routes_list(type):
    url = getUrl(f'/v3/routes/?route_types={type}')
    print(f"Route search url: {url}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        formatted = format(data)
        print(formatted)
        formatted = json.dumps(data, indent=4)
        return(formatted)
    else:
        print(f"Error: {response.status_code} - {response.text}")

def runs_api_request(route_id):
    cache_dir = Path('cache')
    cache_dir.mkdir(exist_ok=True)
    cache_file = cache_dir / f"{route_id}.pkl"
    
    # check if cache exists withing 2 mins
    if cache_file.exists():
        cache_time = os.path.getmtime(cache_file)
        if time.time() - cache_time < 120:
            with open(cache_file, 'rb') as f:
                print(f"Reading from cache for route_id: {route_id}")
                return pickle.load(f)
    
    url = getUrl(f'/v3/runs/route/{route_id}?expand=All')
    print(f"not using cache, search url: {url}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # Save to cache
        with open(cache_file, 'wb') as f:
            pickle.dump(data, f)
        return data
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
        
def runs_ref_api_request(ref):
    url = getUrl(f'/v3/runs/{ref}?expand=All&include_geopath=true')
    print(f"search url: {url}")
    
    response = requests.get(url)
    

    if response.status_code == 200:
        data = response.json()
        return(data)
    else:
        print(f"Error: {response.status_code} - {response.text}")
        # how to get run id for a specific set number?
        
def departures_api_request(stop_id, route_type):
    url = getUrl(f'/v3/departures/route_type/{route_type}/stop/{stop_id}?expand=All')
    print(f"search url: {url}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return(data)
    else:

        print(f"Error: {response.status_code} - {response.text}")
        
        
def route_type_api_request():
    url = getUrl(f'/v3/route_types')
    print(f"search url: {url}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return(data)
    else:

        print(f"Error: {response.status_code} - {response.text}")
        
def disruption_api_request(routeId):
    url = getUrl(f'/v3/disruptions/route/{routeId}')
    print(f"search url: {url}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return(data)
    else:

        print(f"Error: {response.status_code} - {response.text}")
        
def stationDisruption(stop_id):
    url = getUrl(f'/v3/disruptions/stop/{stop_id}')
    print(f"search url: {url}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return(data)
    else:

        print(f"Error: {response.status_code} - {response.text}")
        
def allDisruption():
    url = getUrl(f'/v3/disruptions')
    print(f"search url: {url}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return(data)
    else:

        print(f"Error: {response.status_code} - {response.text}")

       
def specificRunAPIRequest(run_ref, route_type):
    url = getUrl(f'/v3/runs/{run_ref}/route_type/{route_type}?expand=VehiclePosition')
    print(f"search url: {url}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return(data)
    else:

        print(f"Error: {response.status_code} - {response.text}")

def stoppingPatternAPIRequest(run_ref, route_type):
    url = getUrl(f'/v3/pattern/run/{run_ref}/route_type/{route_type}?expand=all&include_skipped_stops=true')
    print(f"search url: {url}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return(data)
    else:

        print(f"Error: {response.status_code} - {response.text}")
        
def stationInfoAPIRequest(stop_id,route_type):
    url = getUrl(f'/v3/stops/{stop_id}/route_type/{route_type}?stop_location=true&stop_amenities=true&stop_accessibility=true&stop_contact=true&stop_ticket=true&stop_staffing=true&stop_disruptions=true')
    print(f"search url: {url}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return(data)
    else:

        print(f"Error: {response.status_code} - {response.text}")
        
def directionAPIrequest(direction_id):
    url = getUrl(f'/v3/directions/{direction_id}')
    print(f"search url: {url}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return(data)
    else:

        print(f"Error: {response.status_code} - {response.text}")

def fareEstimate(minZone:int, maxZone:int, touchOnUTC=None, touchOffUTC=None):
    urlString = f'/v3/fare_estimate/min_zone/{minZone}/max_zone/{maxZone}'
    if touchOnUTC != None:
        if '?' in urlString:
            marker ='&'
        else:
            marker = '?'
        touchOnUTC = touchOnUTC.replace(' ', '%20').replace(":", "%3A")
        urlString += f'{marker}journey_touch_on_utc={touchOnUTC}'

    if touchOffUTC != None:
        if '?' in urlString:
            marker ='&'
        else:
            marker = '?'
        touchOffUTC =touchOffUTC.replace(' ', '%20').replace(":", "%3A")
        urlString += f'{marker}journey_touch_off_utc={touchOffUTC}'


        
    url = getUrl(urlString)
    print(f"search url: {url}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return(data)
    else:

        print(f"Error: {response.status_code} - {response.text}")

def trainData(search_value):
    csv_filename = 'utils/trainsets.csv'
    with open(csv_filename, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row
        for row in reader:
            if row[0] == search_value:
                return row
    return None

def tramData(search_value):
    csv_filename = 'utils/tramsets.csv'
    with open(csv_filename, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row
        for row in reader:
            if row[0] == search_value:
                return row
    return None
