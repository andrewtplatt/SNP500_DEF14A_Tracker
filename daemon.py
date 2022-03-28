import time

import schedule

import d14a_checker
import list_tracker


def run():
    list_tracker.main()
    d14a_checker.main()


def daemon():
    schedule.every().day.at("9").do(run)
    while True:
        time.sleep(60)


if __name__ == '__main__':
    daemon()
