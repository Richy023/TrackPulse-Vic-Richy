import requests
import os
from dotenv import load_dotenv

def upload_image(image_path, number, train_type, location, date, photographer, featured='N', note='', mode='train', exif=None):
    load_dotenv()
    api_token = os.getenv('VRF_TOKEN')
    
    url = 'http://victorianrailphotos.com/api/upload'
    # remember to set this to the actual site when done
    
    data = {
        'number': number,
        'type': train_type,
        'location': location,
        'date': date,
        'photographer': photographer,
        'featured': featured,
        'note': note,
        'mode': mode,
        'exif': exif if exif else None
    }
    
    # Prepare file
    files = {
        'image': (os.path.basename(image_path), open(image_path, 'rb'), 'image/webp')
    }
    
    # Set headers with authorization token
    headers = {
        'Authorization': api_token
    }
    
    try:
        response = requests.post(url, files=files, data=data, headers=headers)
        
        if response.status_code == 200:
            print("Upload successful!")
            print(response.json())
        else:
            print(f"Upload failed with status code {response.status_code}")
            print(response.json())
            
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return {'error': str(e)}
    finally:
        if 'image' in files:
            files['image'][1].close()