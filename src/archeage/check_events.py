import logging
from datetime import datetime, timedelta

import pytz

from src.archeage.event_dates import event_day_time, event_all_day
from src.archeage.mesages import get_event_msg
from src.send_telegram_api import send_message_all

moscow_tz = pytz.timezone('Europe/Moscow')

logger = logging.getLogger("check_events")


# Функция для форматирования timedelta в нужный тон
def format_timedelta_event(td):
    total_seconds = int(td.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    def pluralize(value, one, few, many):
        if 11 <= value % 100 <= 19:
            return many
        elif value % 10 == 1:
            return one
        elif 2 <= value % 10 <= 4:
            return few
        else:
            return many

    minute_part = f"{minutes} {pluralize(minutes, 'минуту', 'минуты', 'минут')}" if minutes > 0 else ""
    second_part = f"{seconds} {pluralize(seconds, 'секунду', 'секунды', 'секунд')}" if seconds > 0 else ""

    if minute_part and second_part:
        return f"{minute_part}, {second_part}"
    elif minute_part:
        return f"{minute_part}"
    elif second_part:
        return f"{second_part}"


# Переменная для отслеживания последнего дня проверки
last_check_date = datetime.now(moscow_tz).date()
sent_notifications = {}


def reset_notifications():
    """Сбрасываем уведомления каждый день."""
    global sent_notifications
    sent_notifications = {}


def daily_check():
    """Ежедневная проверка событий с возможностью сброса уведомлений в полночь."""
    global last_check_date
    now = datetime.now(moscow_tz)

    # Если наступил новый день, сбрасываем уведомления
    if now.date() != last_check_date:
        reset_notifications()
        last_check_date = now.date()

    # Выполняем проверку событий
    check_events()


def check_events():
    """Проверка событий и отправка уведомлений, если событие начнётся через 10 минут или меньше."""
    logger.info("Проверка событий...")
    now = datetime.now(moscow_tz)
    current_weekday = now.weekday()  # Текущий день недели (0 - Понедельник, 6 - Воскресенье)
    current_date = now.date()  # Текущая дата для проверки, было ли уже отправлено уведомление

    # --- Проверка еженедельных событий ---
    for event_name, times in event_day_time.items():
        for weekday, time_str in times:
            if current_weekday == weekday:
                event_time = datetime.strptime(time_str, "%H:%M").time()
                event_datetime = now.replace(hour=event_time.hour, minute=event_time.minute, second=0, microsecond=0)
                difference = event_datetime - now

                # Проверяем, если уже было уведомление для данного события в этот день
                if timedelta(minutes=0) <= difference <= timedelta(minutes=10):
                    event_key = f"{event_name}-{event_time}-{current_date}"
                    if event_key not in sent_notifications:
                        logger.info("Найдено событие: %s", event_name)
                        send_message_all(msg=get_event_msg(event_name, format_timedelta_event(difference)))
                        sent_notifications[event_key] = True  # Отмечаем, что уведомление отправлено

    # --- Проверка ежедневных событий ---
    for event_name, times in event_all_day.items():
        for time_str in times:
            event_time = datetime.strptime(time_str, "%H:%M").time()
            event_datetime = now.replace(hour=event_time.hour, minute=event_time.minute, second=0, microsecond=0)
            difference = event_datetime - now

            if timedelta(minutes=0) <= difference <= timedelta(minutes=10):
                event_key = f"{event_name}-{event_time}-{current_date}"
                if event_key not in sent_notifications:
                    logger.info("Найдено событие: %s", event_name)
                    send_message_all(msg=get_event_msg(event_name, format_timedelta_event(difference)))
                    sent_notifications[event_key] = True  # Отмечаем, что уведомление отправлено

    logger.info("События проверены")
