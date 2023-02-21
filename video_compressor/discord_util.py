import requests
import json 
import uuid
import os
import random

COLORS = ["0xE91E63", "0xFEE75C", "0xE67E22", "0x2ECC71"]

def get_random_file_name():
    return str(uuid.uuid1()) + ".mp4"

def get_random_color():
    return int(COLORS[random.randint(0, len(COLORS) - 1)], 0)

def send_webhook(webhook_url, filepath, fileSize, duration, time_taken):
    success = True
    
    discord_inner = {
        "content": "",
        "embeds": [
            {
                "title": "Video Bot Upload",
                "description": "",
                "color": get_random_color(),
                "fields": [
                    {
                        "name": "Size",
                        "value": str(fileSize) + "(Mb)",
                        "inline": "true"
                    },
                    {
                        "name": "Duration",
                        "value": str(duration) + "(s)",
                        "inline": "true"
                    },
                    {
                        "name": "Time taken",
                        "value": str(time_taken),
                        "inline": "true"

                    }
                        ]
            }
        ]
    }

    discord_payload = {
        "payload_json": json.dumps(discord_inner)
    }

    file_payload = {
        "file": (get_random_file_name(), open(filepath, 'rb'))
    }
    
    try:
        response = requests.post(webhook_url, data=discord_payload, files=file_payload)

        if response.raise_for_status():
            raise Exception()

    except Exception as e:
        print("Caught exception: {}".format(e))
        success = False
        
    return success