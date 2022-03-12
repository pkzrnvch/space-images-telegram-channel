import os
import random
from pathlib import Path
from time import sleep

import telegram
from dotenv import load_dotenv
from fetch_spacex import fetch_spacex_latest_launch
from fetch_nasa import fetch_nasa_apod, fetch_latest_nasa_epic


def post_photo_to_telegram(tg_token, chat_id):
    bot = telegram.Bot(token=tg_token)
    images_to_post = []
    for entry in os.scandir(Path('./images/')):
        if not entry.name.startswith('.') and entry.is_file():
            images_to_post.append(entry.path)
    image_to_post = random.choice(images_to_post)
    with open(image_to_post, 'rb') as image_to_post:
        bot.send_photo(chat_id=chat_id, photo=image_to_post)


def main():
    SECONDS_IN_DAY = 86400
    load_dotenv()
    nasa_token = os.environ.get('NASA_API_KEY')
    tg_token = os.environ.get('TG_TOKEN')
    tg_chat_id = os.environ.get('TG_CHAT_ID')
    seconds_between_posts = int(os.environ.get('SECONDS_BETWEEN_POSTS', SECONDS_IN_DAY))
    fetch_spacex_latest_launch()
    fetch_latest_nasa_epic(nasa_token)
    fetch_nasa_apod(nasa_token)
    while True:
        post_photo_to_telegram(tg_token, tg_chat_id)
        sleep(seconds_between_posts)


if __name__ == '__main__':
    main()
