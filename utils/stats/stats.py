import os, requests, hmac, hashlib, time
import dotenv
import csv

dotenv.load_dotenv()

MEASUREMENT_ID = os.getenv("GOOGLE_ANALYTICS_MEASUREMENT_ID")
API_SECRET = os.getenv('GOOGLE_ANALYTICS_API_SECRET')
HMAC_SECRET = 'because it is my name, because i cannot have another in my life!'.encode()

def log_command(user_id, command_name, guild_id=None):
    def hash_id(id_str):
        return hmac.new(HMAC_SECRET, str(id_str).encode(), hashlib.sha256).hexdigest()
    url = f"https://www.google-analytics.com/mp/collect?measurement_id={MEASUREMENT_ID}&api_secret={API_SECRET}"
    client_id = hash_id(user_id)[:32]
    
    event = {
    "client_id": client_id,
    "events": [
        {
            "name": 'dc_' + command_name.replace('-', '_'),
            "params": {
                "guild_hash": hash_id(guild_id) if guild_id else 'None',
                "user_hash": hash_id(user_id),
                "timestamp_ms": int(time.time() * 1000)
            }
        }
    ]
    }
    
    try:
        r = requests.post(url, json=event, timeout=3)
        if not r.ok:
            print(f"GA tracking failed: {r.status_code} {r.text}")
        else:
            print(f"GA tracking succeeded for command: {command_name}, response: {r.text}")
    except Exception as e:
        print("GA tracking error:", e)
        
    file_path = f"utils/stats/data/{user_id}.csv"
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Command', 'Count'])

    existing_data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            for row in reader:
                existing_data[row[0]] = int(row[1])
    
    current_count = existing_data.get(command_name, 0)
    existing_data[command_name] = current_count + 1

    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Command', 'Count'])  # Write header
        for command, count in existing_data.items():
            writer.writerow([command, count])
    print(f"Logged command {command_name} for user {user_id}")
    
def getFavoriteCommand(userid):
    command_usage = {}
    
    # Read the CSV file
    with open(f'utils/stats/data/{userid}.csv', mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            command = row['Command']
            count = int(row['Count'])
            command_usage[command] = count

    if not command_usage:
        return None, 0

    # Find the command with the highest count
    most_used = max(command_usage, key=command_usage.get)
    count = command_usage[most_used]

    return most_used, count