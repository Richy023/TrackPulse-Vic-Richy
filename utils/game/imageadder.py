import csv
import sqlite3
import os

from photosubmissions.manager import getUserID
from utils.trainlogger.map.uploadimage import uploadImage
from utils.vicrailphotosapi.accepter import convertToWEBP


async def acceptGuesserPhoto(id: int, station: str, difficulty: str, mode: str, username: str):
    # read sql db
    id = str(id)
    conn = sqlite3.connect('photosubmissions/db.db')
    c = conn.cursor()
    c.execute("SELECT * FROM submissions WHERE id = ? ", (id,))
    rows = c.fetchall()
    conn.close()
    
    image_filename = rows[0][2]
    imagePath = f'photosubmissions/photos/{image_filename}'
        
    print('Uploading image to imgbb')
    url = uploadImage(imagePath, name=os.path.splitext(image_filename)[0])
    
    print(f'adding to {mode}.csv: {id}, {station}, {difficulty}')
    with open(f'utils/game/images/{mode}.csv', 'a', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow([url, station, difficulty, username])
