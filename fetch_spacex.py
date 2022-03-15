from pathlib import Path

import requests
from download_and_get_extension import download_image, get_extension


def fetch_spacex_latest_launch():
    spacex_api_url = 'https://api.spacexdata.com/v4/launches/latest'
    response = requests.get(spacex_api_url)
    response.raise_for_status()
    spacex_image_urls = response.json()['links']['flickr']['original']
    for index, url in enumerate(spacex_image_urls, start=1):
        file_path = Path(f'./images/spacex{index}{get_extension(url)}')
        download_image(url, file_path)
