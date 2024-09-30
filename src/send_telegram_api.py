import logging

import requests

from src.config import config

logger = logging.getLogger("send_telegram_api")


def send_message_all(msg):
    for user_id in config.TELEGRAM_USER_IDS:
        url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage?chat_id={user_id}&text={msg}&parse_mode=HTML"
        res = requests.post(url=url)
        logger.info(f"Отправлено сообщение в {user_id}, статус: {res.status_code}")
