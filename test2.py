import time

import schedule


def job():
    print("I'm working...")


schedule.every().at_time()
schedule.every().hour.do(job)
schedule.every().second.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
