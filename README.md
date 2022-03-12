# Telegram space images

This program fetches space photos and uploads them to telegram channel.

### How to install

Create an `.env` file in the project directory. Create a new telegram bot through a BotFather and assign its token to `TG_TOKEN` variable. Create an account on NASA website and generate token to use its API, assign it to `NASA_TOKEN` variable. Assign your telegram channel ID to `TG_CHAT_ID` variable. You can also set `SECONDS_BETWEEN_POSTS` variable to adjust time between posts, which is 86400 seconds (24 hours) by default.

Example of an `.env` file:

```
TELEGRAM_BOT_TOKEN="YOUR_TOKEN"
NASA_TOKEN="YOUR_TOKEN"
TG_CHAT_ID="@chatid"
SECONDS_BETWEEN_POSTS="600"
```

Python3 should already be installed. Use pip (or pip3, in case of conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### Usage

To run the programm use the following command from the project directory:
```
python main.py
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [Devman](https://dvmn.org).