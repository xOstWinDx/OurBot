import time

from src.archeage.check_events import check_events

if __name__ == '__main__':
    while True:
        check_events()
        time.sleep(60)
