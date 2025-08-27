import os
import sqlite3
from PIL import Image
import asyncio

import discord

from photosubmissions.manager import addSubmission
from utils.vicrailphotosapi.vrfAPI import upload_image



async def acceptPhoto(id, username, trainType, featured:bool, note, number, location, date, mode='train'):
    id = str(id)
    conn = sqlite3.connect('photosubmissions/db.db')
    c = conn.cursor()
    c.execute("SELECT * FROM submissions WHERE id = ? ", (id,))
    rows = c.fetchall()
    conn.close()
    if len(rows) == 0:
        return 'No submission found with that ID'
    elif rows[0][6] not in ['both', 'website']:
        return 'This submission is not for the website'
    
    else:
        if number == None:
            number = rows[0][7]
        if location == None:
            location = rows[0][5]
        if date == None:
            date = rows[0][4]
        if note == None:
            note = rows[0][10]
        exif = rows[0][9]
        
        image_filename = rows[0][2]
        image_extension = os.path.splitext(image_filename)[1].lower()
        webp_filename = os.path.splitext(image_filename)[0] + '.webp'

        # Convert the image to WebP
        convertToWEBP(
            input_path=f'photosubmissions/photos/{image_filename}',
            output_path=f'photosubmissions/photos/{webp_filename}'
        )

        print(f'Uploading photo for {username} with number {number}, type {trainType}, location {location}, date {date}, featured: {featured}, note: {note}')
        url = upload_image(
            image_path=f'photosubmissions/photos/{webp_filename}',
            number=number,
            train_type=trainType,
            location=location,
            date=date,
            photographer=username,
            featured='Y' if featured else 'N',
            note=note,
            mode=mode,
            exif=exif,
        )

        if 'error' in url:
            return f'Error uploading photo: {url["error"]}'
        else:
            return 'Photo accepted and uploaded successfully'
    
def convertToWEBP(input_path, output_path, quality=100):

    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file {input_path} does not exist.")
        
        img = Image.open(input_path)
        
        max_size = (1920, 1080)
        if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
        # Convert to RGB if the image is in RGBA
        if img.mode == 'RGBA':
            img = img.convert('RGB')
            
        img.save(output_path, 'WEBP', quality=quality)
        print(f"Image successfully converted to {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")

async def webAddImage(target_guild, target_channel_id, showcase_channel, data):
    print('recieved web image submission, processing...')
    channel = target_guild.get_channel(target_channel_id)
    public_channel = target_guild.get_channel(showcase_channel)
    if channel:
        photo_path = data['filename']
        if os.path.exists(photo_path):
            try:
                file = discord.File(photo_path)
                await public_channel.send(f'New photo submission received from <@{data['username']}>')
                subid, queue = await addSubmission(os.path.basename(photo_path), data['username'], data['date'], data['location'], 'website', data['number'], 0, data.get('exif', None), data.get('note', None))
                await channel.send(f"# Photo submitted for website by <@{data['username']}>:\n- Number: {data['number']}\n- Type:{data['type']}\n- Date: {data['date']}\n- Location: {data['location']}\n- Note: {data['note']}\n<@780303451980038165> ID = `{subid}`", file=file) # type: ignore
                
                # publically send embed
                embed = discord.Embed(title='Photo Submission', 
                description=f'Photo submitted by <@{data['username']}> for website:\n- Number {data['number']}\n- Date: {data['date']}\n- Location: {data['location']}')
                file = discord.File(photo_path, filename=os.path.basename(photo_path))
                embed.set_image(url=f"attachment://{os.path.basename(photo_path)}")
                embed.set_footer(text=f'Position in queue: {queue} | ID: {subid}')
                await public_channel.send(embed=embed, file=file)
            except Exception as e:
                await channel.send(content=f"An error occurred while processing a photo: {str(e)}")
        else:
            print(f"Photo path {photo_path} does not exist.")
    else:
        print(f"Channel with ID {target_channel_id} not found in guild {target_guild.name}")
