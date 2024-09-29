import requests

from src.config import config


def send_message_all(msg):
    for user_id in config.TELEGRAM_USER_IDS:
        url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage?chat_id={user_id}&text={msg}&parse_mode=HTML"
        requests.post(url=url)

