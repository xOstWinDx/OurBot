from datetime import datetime, timedelta

import pytz

from src.archeage.event_dates import event_day_time, event_all_day

moscow_tz = pytz.timezone('Europe/Moscow')


def check_events():
    now = datetime.now(moscow_tz)
    current_weekday = now.weekday()  # Текущий день недели (0 - Понедельник, 6 - Воскресенье)

    # --- Проверка еженедельных событий ---
    for event_name, times in event_day_time.items():
        for weekday, time_str in times:
            if current_weekday == weekday:
                event_time = datetime.strptime(time_str, "%H:%M").time()
                event_datetime = now.replace(hour=event_time.hour, minute=event_time.minute, second=0, microsecond=0)
                difference = event_datetime - now

                if timedelta(minutes=0) <= difference <= timedelta(minutes=10):
                    print(f"Событие '{event_name}' наступит через {difference.total_seconds() / 60:.2f} минут!")
                    # Здесь можно выполнить действие

    # --- Проверка ежедневных событий ---
    for event_name, times in event_all_day.items():
        for time_str in times:
            event_time = datetime.strptime(time_str, "%H:%M").time()
            event_datetime = now.replace(hour=event_time.hour, minute=event_time.minute, second=0, microsecond=0)
            difference = event_datetime - now

            if timedelta(minutes=0) <= difference <= timedelta(minutes=10):
                print(
                    f"Событие '{event_name}' (ежедневное) наступит через {difference.total_seconds() / 60:.2f} минут!")
                # Здесь можно выполнить действие
