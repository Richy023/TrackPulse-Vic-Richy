import requests
import os
from dotenv import load_dotenv

load_dotenv()
WEB_BASE_URL = os.getenv('WEB_BASE_URL')

def logTrip(mode, userid:int, start=None, end=None, line=None, number=None, vType=None, date=None, note=None, tags=None):
    """
    Logs a trip with the given parameters.

    Parameters:
    - userid (int): Discord user ID.

    Returns:
    None
    """
    if not WEB_BASE_URL:
        print("WEB_BASE_URL is not set in the environment variables.")
        return 'error'
    
    # format user id
    userid = f'oauth2|discord|{userid}'
    
    data = {
        'mode': mode,
        'userid': userid,
        'start': start,
        'end': end,
        'line': line,
        'number': number,
        'type': vType,
        'date': date,
        'tags': tags
    }
    
    if note != None:
        data['note'] = note

    try:
        response = requests.post(f"{WEB_BASE_URL}/addLog", data=data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error logging trip: {e}")
        return 'error'
        
    return response.json() if response.status_code == 200 else None
    
def getUserCSV(username):
    if not WEB_BASE_URL:
        print("WEB_BASE_URL is not set in the environment variables.")
        return 'error'
    
    try:
        response = requests.get(f"{WEB_BASE_URL}/getCSV", params={'username': username})
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error retrieving CSV: {e}")
        return 'error'
        
    return response.text if response.status_code == 200 else None