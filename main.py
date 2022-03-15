import os
import random
from pathlib import Path
from time import sleep

import telegram
from dotenv import load_dotenv
from fetch_spacex import fetch_spacex_latest_launch
from fetch_nasa import fetch_nasa_apod, fetch_latest_nasa_epic


def choose_photo_to_post():
    images_to_post = []
    for entry in os.scandir('./images/'):
        if not entry.name.startswith('.') and entry.is_file():
            images_to_post.append(entry.path)
    image_to_post = random.choice(images_to_post)
    return image_to_post


def post_photo_to_telegram(tg_token, chat_id):
    bot = telegram.Bot(token=tg_token)
    image_to_post = choose_photo_to_post()
    with open(image_to_post, 'rb') as image_to_post:
        bot.send_photo(chat_id=chat_id, photo=image_to_post)


def main():
    load_dotenv()
    nasa_token = os.environ.get('NASA_API_KEY')
    tg_token = os.environ.get('TG_TOKEN')
    tg_chat_id = os.environ.get('TG_CHAT_ID')
    seconds_in_day = 86400
    seconds_between_posts = int(os.environ.get('SECONDS_BETWEEN_POSTS', seconds_in_day))
    photo_folder = Path('./images')
    photo_folder.mkdir(exist_ok=True)
    fetch_spacex_latest_launch()
    fetch_latest_nasa_epic(nasa_token)
    fetch_nasa_apod(nasa_token)
    while True:
        post_photo_to_telegram(tg_token, tg_chat_id)
        sleep(seconds_between_posts)


if __name__ == '__main__':
    main()
