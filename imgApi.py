import requests
import json
from io import BytesIO

URL = "https://serpapi.com/search.json?engine=yandex_images&text={0}&api_key=d521ba18ea4e93e1570f476ece91918871b21eb4ba52ca7d0731764bb80e9cf7"


def searchImages(query):
    img_urls = []
    req_url = URL.format(query)
    res = requests.get(req_url)
    response_json = json.loads(res.text)
    for image in response_json['images_results']:
        img_urls.append(image['original'])
    return img_urls

def getImageData(image_url):
    image_resp = requests.get(image_url)
    return BytesIO(image_resp.content)
