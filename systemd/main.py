import logging
import time

from src.archeage.check_events import daily_check

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    while True:
        daily_check()
        time.sleep(60)
