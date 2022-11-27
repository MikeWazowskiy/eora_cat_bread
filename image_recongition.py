import json
import requests

api_key = 'acc_4633029162d9a16'
api_secret = 'd7d122e76ff0e2c4ed1c270a5525b13f'

def image_recognize(image):
    tags = []

    response = requests.post(
        'https://api.imagga.com/v2/tags',
        auth=(api_key, api_secret),
        files={'image': open(image, 'rb')})

    data = json.loads(response.text.encode("ascii"))

    for i in range(6):
        tag = data['result']['tags'][i]['tag']['en']
        tags.append(tag)

    return tags