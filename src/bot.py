from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from src.config import config

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
