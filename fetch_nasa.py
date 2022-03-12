import datetime
from pathlib import Path

import requests
from download_and_get_extension import download_image, get_extension


def fetch_nasa_apod(nasa_token, count=25):
    payload = {
        'api_key': nasa_token,
        'count': count,
             }
    nasa_apod_api_url = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(nasa_apod_api_url, params=payload)
    response.raise_for_status()
    apod_images_urls = []
    for element in response.json():
        apod_images_urls.append(element['url'])
    for index, url in enumerate(apod_images_urls):
        file_path = Path(f'./images/apod{index + 1}{get_extension(url)}')
        download_image(url, file_path)


def fetch_latest_nasa_epic(nasa_token):
    payload = {'api_key': nasa_token}
    nasa_epic_api_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    response = requests.get(nasa_epic_api_url, params=payload)
    response.raise_for_status()
    epic_images_metadata = response.json()
    epic_images_urls = []
    for image_metadata in epic_images_metadata:
        image_datetime = datetime.datetime.fromisoformat(image_metadata['date'])
        image_name = image_metadata['image']
        image_url = 'https://api.nasa.gov/EPIC/archive/natural/'\
                    f'{image_datetime:%Y/%m/%d}/png/{image_name}.png'
        epic_images_urls.append(image_url)
    for index, url in enumerate(epic_images_urls):
        file_path = Path(f'./images/epic{index + 1}{get_extension(url)}')
        download_image(url, file_path, payload=payload)