import datetime
import os
from pathlib import Path
from urllib.parse import urlsplit
import requests
from dotenv import load_dotenv
import telegram


def download_image(image_url, file_path, payload=None):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(image_url, params=payload)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)


def get_extension(image_url):
    split_url = urlsplit(image_url)
    url_path = Path(split_url.path)
    extension = url_path.suffix
    return extension


def fetch_spacex_latest_launch():
    spacex_api_url = 'https://api.spacexdata.com/v4/launches/latest'
    response = requests.get(spacex_api_url)
    response.raise_for_status()
    print(response.json())
    spacex_image_urls = response.json()['links']['flickr']['original']
    print(spacex_image_urls)
    for index, url in enumerate(spacex_image_urls):
        file_path = Path(f'./images/spacex{index + 1}{get_extension(url)}')
        download_image(url, file_path)


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
        apod_images_urls.append(element['hdurl'])
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
    print(epic_images_urls)
    for index, url in enumerate(epic_images_urls):
        file_path = Path(f'./images/epic{index + 1}{get_extension(url)}')
        download_image(url, file_path, payload=payload)


def telegram_channel_post(message, tg_token, chat_id='@Wowspacephotos'):
    bot = telegram.Bot(token=tg_token)
    bot.send_message(text=message, chat_id=chat_id)

def main():
    load_dotenv()
    nasa_token = os.getenv('NASA_API_KEY')
    tg_token = os.getenv('TG_TOKEN')
    #fetch_spacex_latest_launch()
    #fetch_latest_nasa_epic(nasa_token)
    #fetch_nasa_apod(nasa_token)
    telegram_channel_post('Space', tg_token)


if __name__ == '__main__':
    main()
